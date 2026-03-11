"""
Local LLM Interface with Ollama
A Streamlit application for interacting with local LLM models via Ollama.

Features:
- Dynamic perspective and audience settings for contextualized responses
- Question template system with pre-defined scientific/educational prompts
- Chat history with HTML export capabilities
- Configurable model parameters (temperature, top-k, top-p, context length)
"""

import re
import streamlit as st
import requests
import html
from typing import List, Tuple, Optional

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)

# Import our utility modules
from utils.template_manager import TemplateManager
from utils.prompt_builder import PromptBuilder
from utils.html_export import build_pair_html, build_conversation_html, safe_filename
from utils.document_processor import DocumentProcessor

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Local LLM Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Initialize Template Manager
# -----------------------------
@st.cache_resource
def get_template_manager():
    """Initialize and cache the template manager."""
    return TemplateManager()

template_manager = get_template_manager()

# -----------------------------
# Helper Functions
# -----------------------------
def get_local_models() -> List[str]:
    """
    Fetch available Ollama models from local instance.
    
    Returns:
        List of model names, or empty list if unavailable
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except Exception as e:
        st.error(f"Error fetching models: {e}")
    return []

def generate_ai_response(user_input: str, perspective: str, audience: str, 
                        llm_engine, chat_history: List[Tuple[str, str]], 
                        has_documents: bool = False) -> str:
    """
    Generate AI response using the LLM with context-aware system prompt.
    
    Args:
        user_input: User's question/prompt
        perspective: Selected perspective (who's writing)
        audience: Selected audience (who's reading)
        llm_engine: Configured ChatOllama instance
        chat_history: Previous conversation history
        has_documents: Whether documents are uploaded (enables strict RAG mode)
        
    Returns:
        AI-generated response string
    """
    # Build dynamic system prompt based on perspective, audience, and document presence
    system_prompt_text = PromptBuilder.build_system_prompt(perspective, audience, has_documents)
    system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)
    
    # Build conversation history (limit to last 5 exchanges for context window management)
    conversation_history = []
    for past_query, past_response in chat_history[-5:]:
        conversation_history.append(HumanMessage(content=past_query))
        conversation_history.append(AIMessage(content=past_response))

    # Add current user input
    conversation_history.append(HumanMessage(content=user_input))

    # Create prompt chain and invoke
    prompt_chain = ChatPromptTemplate.from_messages([system_prompt] + conversation_history)
    return (prompt_chain | llm_engine | StrOutputParser()).invoke({})

def generate_followup_questions(user_input: str, ai_response: str, llm_engine) -> List[str]:
    """
    Generate 3 suggested follow-up questions based on a Q&A pair.

    Args:
        user_input: The user's original question
        ai_response: The AI's response
        llm_engine: Configured ChatOllama instance

    Returns:
        List of up to 3 follow-up question strings
    """
    prompt = (
        "Based on the following question and answer, generate exactly 3 insightful "
        "follow-up questions that would deepen understanding of the topic. "
        "Return only the 3 questions, one per line, numbered 1. 2. 3. "
        "Do not include any other text or explanation.\n\n"
        f"Question: {user_input}\n\n"
        f"Answer: {ai_response}\n\n"
        "Follow-up questions:"
    )
    try:
        result = llm_engine.invoke([HumanMessage(content=prompt)])
        raw = result.content if hasattr(result, "content") else str(result)

        questions = []
        for line in raw.strip().split("\n"):
            line = line.strip()
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
            if cleaned:
                questions.append(cleaned)

        return questions[:3]
    except Exception:
        return []

# -----------------------------
# Session State Initialization
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List of (user_query, ai_response) tuples

if "perspective" not in st.session_state:
    st.session_state.perspective = "Scientist"

if "audience" not in st.session_state:
    st.session_state.audience = "Scientist"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Chat"

if "selected_template" not in st.session_state:
    st.session_state.selected_template = None

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if "document_content" not in st.session_state:
    st.session_state.document_content = ""

if "allow_llm_knowledge" not in st.session_state:
    st.session_state.allow_llm_knowledge = False  # RAG-first: disabled by default (unchecked)

if "followup_questions" not in st.session_state:
    st.session_state.followup_questions = {}  # Dict: chat_history index -> List[str]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None  # Follow-up question clicked by user

# -----------------------------
# Navigation
# -----------------------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Chat", "Manage Templates"],
    key="navigation",
    index=0 if st.session_state.current_page == "Chat" else 1
)
st.session_state.current_page = page

# -----------------------------
# Sidebar: Perspective & Audience (applies to whole conversation)
# -----------------------------
st.sidebar.title("🎭 Context Settings")
st.sidebar.markdown("*These settings apply to the entire conversation*")

perspectives = PromptBuilder.get_available_perspectives()
st.session_state.perspective = st.sidebar.selectbox(
    "Perspective (Who is writing):",
    perspectives,
    index=perspectives.index(st.session_state.perspective),
    help="Select who should be explaining/writing the answers"
)

audiences = PromptBuilder.get_available_audiences()
st.session_state.audience = st.sidebar.selectbox(
    "Audience (Who is reading):",
    audiences,
    index=audiences.index(st.session_state.audience),
    help="Select who the explanations should be tailored for"
)

# -----------------------------
# Sidebar: RAG Mode Control
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.title("🎯 Answer Source")

# Show different UI based on whether documents are loaded
if st.session_state.document_content:
    st.sidebar.success("📄 Documents Loaded - RAG Mode Active")
    st.sidebar.markdown("**Answer source:** Uploaded documents")
    
    st.session_state.allow_llm_knowledge = st.sidebar.checkbox(
        "☑️ Allow LLM General Knowledge",
        value=st.session_state.allow_llm_knowledge,
        help="Enable this to allow the AI to supplement answers with its general knowledge. "
             "When disabled (default), AI answers ONLY from your uploaded documents."
    )
    
    if st.session_state.allow_llm_knowledge:
        st.sidebar.warning("⚠️ AI can use general knowledge + documents")
    else:
        st.sidebar.info("✅ AI will answer ONLY from documents")
else:
    st.sidebar.info("📝 No Documents - LLM Mode")
    st.sidebar.markdown("**Answer source:** LLM general knowledge")
    st.sidebar.markdown("*Upload documents to enable RAG mode*")
    # Automatically enable LLM knowledge when no documents
    st.session_state.allow_llm_knowledge = True

# -----------------------------
# Sidebar: Model Settings
# -----------------------------
st.sidebar.title("⚙️ Model Settings")
model_options = get_local_models()

if not model_options:
    st.sidebar.error("⚠️ No models available. Ensure Ollama is running.")
    selected_model = None
else:
    selected_model = st.sidebar.selectbox(
        "Select Model:",
        model_options,
        index=0,
        help="Choose which LLM model to use"
    )

temperature = st.sidebar.slider(
    "Temperature:",
    0.0, 2.0, 0.3, 0.05,
    help="Controls randomness: lower = more focused, higher = more creative"
)

top_k = st.sidebar.slider(
    "Top-K:",
    1, 100, 40, 1,
    help="Number of highest probability tokens to consider"
)

top_p = st.sidebar.slider(
    "Top-P:",
    0.0, 1.0, 0.9, 0.01,
    help="Nucleus sampling threshold"
)

num_ctx = st.sidebar.slider(
    "Context Length:",
    256, 8192, 2048, 256,
    help="Maximum context window size"
)

# Initialize LLM engine if model is selected
llm_engine = None
if selected_model:
    llm_engine = ChatOllama(
        model=selected_model,
        base_url="http://localhost:11434",
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        num_ctx=num_ctx
    )

# -----------------------------
# Sidebar: Question History
# -----------------------------
if st.session_state.chat_history:
    st.sidebar.title("❓ Questions Asked")
    for i, (query, _) in enumerate(st.session_state.chat_history):
        # Truncate long queries for display
        display_query = query[:50] + "..." if len(query) > 50 else query
        st.sidebar.markdown(f"[**{i+1}.** {display_query}](#question-{i})")
        st.sidebar.markdown("---")

# =============================================================================
# PAGE 1: CHAT INTERFACE
# =============================================================================
if page == "Chat":
    st.title("🔬 Local LLM Scientific Assistant")
    
    # Show current mode with clear visual indicators
    if st.session_state.document_content:
        if st.session_state.allow_llm_knowledge:
            st.warning("⚠️ **HYBRID MODE**: AI will use documents + general knowledge")
            st.caption(f"🎯 **Perspective:** {st.session_state.perspective} | **Audience:** {st.session_state.audience} | **Documents:** {len(st.session_state.uploaded_documents)} | **Mode:** Hybrid")
        else:
            st.success("✅ **STRICT RAG MODE**: AI will answer ONLY from your uploaded documents")
            st.caption(f"🎯 **Perspective:** {st.session_state.perspective} | **Audience:** {st.session_state.audience} | **Documents:** {len(st.session_state.uploaded_documents)} | **Mode:** RAG Only")
    else:
        st.info("💬 **LLM MODE**: AI will use general knowledge (upload documents for RAG mode)")
        st.caption(f"🎯 **Perspective:** {st.session_state.perspective} | **Audience:** {st.session_state.audience}")
    
    # -----------------------------
    # Document Upload Section
    # -----------------------------
    with st.expander("📄 Upload Documents (PDF, DOCX, PPTX)", expanded=False):
        st.markdown("*Upload documents to include their content in your queries*")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose PDF, DOCX, or PPTX files",
            type=['pdf', 'docx', 'doc', 'pptx'],
            accept_multiple_files=True,
            help="Upload one or more documents. Maximum 200 MB per file.",
            key="document_uploader"
        )
        
        # Process uploaded files
        if uploaded_files:
            if st.button("📥 Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    results = DocumentProcessor.process_multiple_documents(uploaded_files)
                    st.session_state.uploaded_documents = results

                    # Format content for use in queries
                    st.session_state.document_content = DocumentProcessor.format_document_content(
                        results,
                        include_filenames=True
                    )

                    # Reset to STRICT RAG MODE when documents are loaded
                    st.session_state.allow_llm_knowledge = False
                    
                    # Show summary
                    st.success("Documents processed!")
                    for result in results:
                        summary = DocumentProcessor.get_document_summary(result)
                        if result['error']:
                            st.error(summary)
                        else:
                            st.info(summary)
                    
                    # Rerun to update the UI and show RAG mode indicator
                    st.rerun()
        
        # Display currently loaded documents
        if st.session_state.uploaded_documents:
            st.markdown("---")
            st.markdown("**Currently Loaded Documents:**")
            
            for i, result in enumerate(st.session_state.uploaded_documents):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if result['error']:
                        st.markdown(f"❌ {result['filename']} - *Error*")
                    else:
                        word_count = len(result['content'].split())
                        st.markdown(f"✅ {result['filename']} (~{word_count:,} words)")
                with col2:
                    if st.button("🗑️", key=f"remove_doc_{i}", help="Remove this document"):
                        st.session_state.uploaded_documents.pop(i)
                        # Reformat content
                        st.session_state.document_content = DocumentProcessor.format_document_content(
                            st.session_state.uploaded_documents,
                            include_filenames=True
                        )
                        st.rerun()
            
            # Clear all button
            if st.button("🗑️ Clear All Documents", type="secondary"):
                st.session_state.uploaded_documents = []
                st.session_state.document_content = ""
                st.rerun()
            
            # Preview toggle
            if st.checkbox("👁️ Preview Document Content", key="preview_docs"):
                st.markdown("**Document Content Preview:**")
                preview_text = st.session_state.document_content[:2000]
                if len(st.session_state.document_content) > 2000:
                    preview_text += f"\n\n... ({len(st.session_state.document_content) - 2000:,} more characters)"
                st.text_area(
                    "Content",
                    preview_text,
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
    
    # -----------------------------
    # Question Templates Section
    # -----------------------------
    with st.expander("📋 Question Templates", expanded=False):
        st.markdown("*Select a pre-defined question template or ask your own*")
        
        # Load templates and organize by category
        all_templates = template_manager.load_templates()
        categories = template_manager.get_all_categories()
        
        # Category filter
        selected_category = st.selectbox(
            "Filter by Category:",
            ["All"] + categories,
            key="category_filter"
        )
        
        # Filter templates by category
        if selected_category == "All":
            filtered_templates = all_templates
        else:
            filtered_templates = template_manager.get_templates_by_category(selected_category)
        
        if filtered_templates:
            # Create template selector
            template_names = [t["name"] for t in filtered_templates]
            selected_template_name = st.selectbox(
                "Select Template:",
                ["-- None --"] + template_names,
                key="template_selector"
            )
            
            if selected_template_name != "-- None --":
                selected_template = template_manager.get_template_by_name(selected_template_name)
                
                if selected_template:
                    # Display template details
                    st.info(f"**Description:** {selected_template.get('description', 'No description available')}")
                    st.markdown(f"**Template:** {selected_template['template']}")
                    
                    # Two options for using the template
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📝 Use Template with Form", use_container_width=True):
                            st.session_state.selected_template = selected_template
                            st.rerun()
                    
                    with col2:
                        if st.button("💬 Populate Chat Input", use_container_width=True):
                            # This will populate the chat input below
                            st.session_state.template_text = selected_template['template']
                            st.success("✅ Template populated in chat input below!")
        else:
            st.info("No templates available in this category.")
    
    # -----------------------------
    # Template Input Form (if template selected)
    # -----------------------------
    if st.session_state.selected_template:
        with st.form("template_form"):
            st.subheader(f"📋 {st.session_state.selected_template['name']}")
            st.markdown(f"*{st.session_state.selected_template.get('description', '')}*")
            
            # Show the template text
            st.markdown(f"**Question:** {st.session_state.selected_template['template']}")
            
            # Get user input if required
            user_content = ""
            if st.session_state.selected_template.get('requires_input', True):
                user_content = st.text_area(
                    st.session_state.selected_template.get('input_label', 'Enter your content:'),
                    height=150,
                    key="template_content_input"
                )
            
            col1, col2 = st.columns([1, 1])
            submit = col1.form_submit_button("🚀 Submit Question", use_container_width=True)
            cancel = col2.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if st.session_state.selected_template.get('requires_input', True) and not user_content.strip():
                    st.error("Please provide the required input.")
                else:
                    # Combine template and content
                    if user_content.strip():
                        base_query = f"{st.session_state.selected_template['template']}\n\n{user_content}"
                    else:
                        base_query = st.session_state.selected_template['template']
                    
                    # RAG-first enforcement
                    has_docs = bool(st.session_state.document_content)
                    can_answer = has_docs or st.session_state.allow_llm_knowledge
                    
                    if not can_answer:
                        st.error("⚠️ **No documents uploaded!** Please upload documents to get answers, or enable 'Allow LLM General Knowledge' in the sidebar.")
                    else:
                        # Format query based on mode
                        if has_docs and not st.session_state.allow_llm_knowledge:
                            # STRICT RAG MODE
                            full_query = f"""You are in STRICT DOCUMENT-ONLY mode. You must answer EXCLUSIVELY from the document content below. Do not use any external knowledge.

DOCUMENT CONTENT:
{st.session_state.document_content}

============================================================

USER QUESTION: {base_query}

REMINDER: Answer using ONLY the document content above. If the answer is not in the document, state: "This information is not found in the provided document." Cite specific sections or use direct quotes."""
                        
                        elif has_docs and st.session_state.allow_llm_knowledge:
                            # HYBRID MODE
                            full_query = f"""You have access to both uploaded document content and your general knowledge.

DOCUMENT CONTENT:
{st.session_state.document_content}

============================================================

USER QUESTION: {base_query}

INSTRUCTIONS: Prioritize information from the document when available. You may supplement with your general knowledge if helpful. Clearly distinguish between information from the document versus your general knowledge."""
                        
                        else:
                            # LLM MODE
                            full_query = base_query
                        
                        # Generate response
                        if llm_engine:
                            with st.spinner("🤔 Generating response..."):
                                response = generate_ai_response(
                                    full_query,
                                    st.session_state.perspective,
                                    st.session_state.audience,
                                    llm_engine,
                                    st.session_state.chat_history,
                                    has_documents=has_docs
                                )
                                # Store the BASE query
                                st.session_state.chat_history.append((base_query, response))
                                # Generate and store follow-up questions for this exchange
                                followups = generate_followup_questions(base_query, response, llm_engine)
                                if followups:
                                    st.session_state.followup_questions[len(st.session_state.chat_history) - 1] = followups
                                st.session_state.selected_template = None
                                st.rerun()
                        else:
                            st.error("No model selected. Please select a model in the sidebar.")
            
            if cancel:
                st.session_state.selected_template = None
                st.rerun()
    
    # -----------------------------
    # Chat Input
    # -----------------------------
    # Check if we have template text to populate
    initial_input = st.session_state.get('template_text', '')
    if initial_input:
        # Clear it after reading
        del st.session_state.template_text
    
    user_query = st.chat_input(
        "Type your query here or use a template above...",
        key="main_chat_input"
    )

    # If a follow-up question button was clicked, treat it as the user query
    if not user_query and st.session_state.pending_query:
        user_query = st.session_state.pending_query
        st.session_state.pending_query = None

    if user_query:
        if llm_engine:
            # RAG-first enforcement: Check if we can answer
            has_docs = bool(st.session_state.document_content)
            can_answer = has_docs or st.session_state.allow_llm_knowledge
            
            if not can_answer:
                # RAG mode but no documents - cannot answer
                st.error("⚠️ **No documents uploaded!** Please upload documents to get answers, or enable 'Allow LLM General Knowledge' in the sidebar.")
            else:
                with st.spinner("🤔 Processing your question..."):
                    # Format query based on mode
                    if has_docs and not st.session_state.allow_llm_knowledge:
                        # STRICT RAG MODE: Only document content
                        full_query = f"""You are in STRICT DOCUMENT-ONLY mode. You must answer EXCLUSIVELY from the document content below. Do not use any external knowledge.

DOCUMENT CONTENT:
{st.session_state.document_content}

============================================================

USER QUESTION: {user_query}

REMINDER: Answer using ONLY the document content above. If the answer is not in the document, state: "This information is not found in the provided document." Cite specific sections or use direct quotes."""
                    
                    elif has_docs and st.session_state.allow_llm_knowledge:
                        # HYBRID MODE: Document + general knowledge allowed
                        full_query = f"""You have access to both uploaded document content and your general knowledge.

DOCUMENT CONTENT:
{st.session_state.document_content}

============================================================

USER QUESTION: {user_query}

INSTRUCTIONS: Prioritize information from the document when available. You may supplement with your general knowledge if helpful. Clearly distinguish between information from the document versus your general knowledge."""
                    
                    else:
                        # LLM MODE: No documents, general knowledge only
                        full_query = user_query
                    
                    response = generate_ai_response(
                        full_query,
                        st.session_state.perspective,
                        st.session_state.audience,
                        llm_engine,
                        st.session_state.chat_history,
                        has_documents=has_docs
                    )
                    # Store the ORIGINAL user query
                    st.session_state.chat_history.append((user_query, response))
                    # Generate and store follow-up questions for this exchange
                    followups = generate_followup_questions(user_query, response, llm_engine)
                    if followups:
                        st.session_state.followup_questions[len(st.session_state.chat_history) - 1] = followups
                    st.rerun()
        else:
            st.error("⚠️ No model selected. Please select a model in the sidebar.")
    
    # -----------------------------
    # Display Conversation History
    # -----------------------------
    st.markdown("---")
    st.header("💬 Conversation History")
    
    if st.session_state.chat_history:
        # Full conversation export button
        full_html = build_conversation_html(
            st.session_state.chat_history,
            title="Conversation Transcript",
            perspective=st.session_state.perspective,
            audience=st.session_state.audience
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.download_button(
                label="⬇️ Download Full Conversation (HTML)",
                data=full_html.encode("utf-8"),
                file_name=safe_filename("conversation_transcript"),
                mime="text/html",
                use_container_width=True
            )
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        st.markdown("---")
        
        # Display each Q&A pair
        for i, (query, response) in enumerate(st.session_state.chat_history):
            # Create anchor for sidebar navigation
            st.markdown(f"<a name='question-{i}'></a>", unsafe_allow_html=True)
            
            # User question
            with st.container():
                st.markdown(f"### 👤 You (Question #{i+1})")
                st.markdown(query)
            
            # AI response
            with st.container():
                st.markdown(f"### 🤖 AI Response")
                st.markdown(response)

            # Suggested follow-up questions
            followups = st.session_state.followup_questions.get(i, [])
            if followups:
                st.markdown("**💡 Suggested Follow-up Questions:**")
                for j, fq in enumerate(followups):
                    if st.button(f"❓ {fq}", key=f"followup-{i}-{j}"):
                        st.session_state.pending_query = fq
                        st.rerun()

            # Download individual Q&A
            pair_html = build_pair_html(
                i, query, response,
                perspective=st.session_state.perspective,
                audience=st.session_state.audience
            )
            st.download_button(
                label=f"⬇️ Download Q&A #{i+1} (HTML)",
                data=pair_html.encode("utf-8"),
                file_name=safe_filename(f"qa_{i+1}"),
                mime="text/html",
                key=f"dl-qapair-{i}",
                use_container_width=False
            )
            
            st.markdown("---")
    else:
        st.info("👋 No conversation yet. Ask a question to get started!")

# =============================================================================
# PAGE 2: TEMPLATE MANAGEMENT
# =============================================================================
elif page == "Manage Templates":
    st.title("📚 Template Management")
    st.markdown("*Create, edit, and organize your question templates*")
    
    # Create tabs for different template operations
    tab1, tab2, tab3 = st.tabs(["📋 View Templates", "➕ Add Template", "🔧 Settings"])
    
    # -----------------------------
    # TAB 1: View/Delete Templates
    # -----------------------------
    with tab1:
        st.header("All Templates")
        
        all_templates = template_manager.load_templates()
        categories = template_manager.get_all_categories()
        
        # Category filter
        view_category = st.selectbox(
            "Filter by Category:",
            ["All"] + categories,
            key="view_category_filter"
        )
        
        # Filter templates
        if view_category == "All":
            display_templates = all_templates
        else:
            display_templates = template_manager.get_templates_by_category(view_category)
        
        if display_templates:
            st.markdown(f"**Total Templates:** {len(display_templates)}")
            
            # Display templates in expandable sections
            for template in display_templates:
                with st.expander(f"📌 {template['name']} ({template.get('category', 'Uncategorized')})"):
                    st.markdown(f"**ID:** `{template['id']}`")
                    st.markdown(f"**Category:** {template.get('category', 'Uncategorized')}")
                    st.markdown(f"**Description:** {template.get('description', 'No description')}")
                    st.markdown(f"**Template Text:**")
                    st.code(template['template'], language=None)
                    st.markdown(f"**Requires Input:** {'Yes' if template.get('requires_input', True) else 'No'}")
                    
                    if template.get('requires_input', True):
                        st.markdown(f"**Input Label:** {template.get('input_label', 'N/A')}")
                    
                    # Delete button
                    if st.button(f"🗑️ Delete Template", key=f"delete_{template['id']}"):
                        if template_manager.delete_template(template['id']):
                            st.success(f"✅ Deleted template: {template['name']}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete template")
        else:
            st.info("No templates found in this category.")
    
    # -----------------------------
    # TAB 2: Add New Template
    # -----------------------------
    with tab2:
        st.header("Create New Template")
        
        with st.form("add_template_form"):
            new_name = st.text_input(
                "Template Name*:",
                help="Give your template a descriptive name"
            )
            
            new_category = st.selectbox(
                "Category*:",
                ["Research", "Teaching", "Laboratory", "Research Design", 
                 "Statistics", "Critical Thinking", "Career", "General", "Custom"],
                help="Organize templates by category"
            )
            
            new_template = st.text_area(
                "Template Text*:",
                height=150,
                help="The question or prompt text. Use clear, specific language."
            )
            
            new_description = st.text_area(
                "Description:",
                height=80,
                help="Brief description of what this template does (optional but recommended)"
            )
            
            new_requires_input = st.checkbox(
                "Requires user input",
                value=True,
                help="Check if this template needs additional content from the user"
            )
            
            new_input_label = ""
            if new_requires_input:
                new_input_label = st.text_input(
                    "Input Label:",
                    value="Enter your content:",
                    help="Label for the input field when using this template"
                )
            
            submitted = st.form_submit_button("➕ Add Template", use_container_width=True)
            
            if submitted:
                if not new_name.strip():
                    st.error("❌ Template name is required")
                elif not new_template.strip():
                    st.error("❌ Template text is required")
                else:
                    success = template_manager.add_template(
                        name=new_name.strip(),
                        template=new_template.strip(),
                        category=new_category,
                        requires_input=new_requires_input,
                        input_label=new_input_label,
                        description=new_description.strip()
                    )
                    
                    if success:
                        st.success(f"✅ Successfully added template: {new_name}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to add template")
    
    # -----------------------------
    # TAB 3: Settings
    # -----------------------------
    with tab3:
        st.header("Template Settings")
        
        st.subheader("📊 Statistics")
        all_templates = template_manager.load_templates()
        categories = template_manager.get_all_categories()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Templates", len(all_templates))
        with col2:
            st.metric("Categories", len(categories))
        
        st.markdown("---")
        
        st.subheader("⚠️ Danger Zone")
        st.warning("**Warning:** The following action cannot be undone!")
        
        if st.button("🔄 Reset to Default Templates", type="secondary"):
            st.session_state.confirm_reset = True
        
        if st.session_state.get('confirm_reset', False):
            st.error("**Are you sure?** This will delete all custom templates and restore defaults.")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Yes, Reset", type="primary"):
                    if template_manager.reset_to_defaults():
                        st.success("✅ Templates reset to defaults")
                        st.session_state.confirm_reset = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to reset templates")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.confirm_reset = False
                    st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    <p>🔬 Local LLM Scientific Assistant</p>
    <p>Powered by Ollama & Streamlit</p>
</div>
""", unsafe_allow_html=True)
