# 📦 Project Overview - Complete File Guide

## 🎯 What You Received

A complete, production-ready Streamlit application for interacting with local LLMs via Ollama, specifically designed for scientific and educational use. The application has been thoroughly refactored from your original code with significant new features added.

---

## 📁 File Structure & Purpose

```
ollama_app/                              📦 Main project directory
│
├── 🚀 QUICKSTART FILES (Start Here!)
│   ├── QUICKSTART.md                    ⭐ 5-minute setup guide - READ THIS FIRST
│   └── README.md                        📘 Comprehensive documentation
│
├── 🔧 APPLICATION FILES (Core Code)
│   ├── app.py                           💻 Main Streamlit application (468 lines)
│   └── requirements.txt                 📋 Python dependencies
│
├── 📚 DOCUMENTATION FILES
│   ├── IMPLEMENTATION_SUMMARY.md        📊 Detailed implementation report
│   ├── ARCHITECTURE.md                  🏗️  Visual system architecture
│   ├── CHANGELOG.md                     📝 Changes from original code
│   └── TROUBLESHOOTING.md              🔧 Comprehensive problem-solving guide
│
├── ⚙️ CONFIG FILES (Template Storage)
│   └── config/
│       └── default_templates.json       🎯 30 built-in question templates
│       # question_templates.json        (Auto-created on first run)
│
└── 🛠️ UTILITY MODULES (Backend Logic)
    └── utils/
        ├── __init__.py                  📦 Package initialization
        ├── template_manager.py          🗂️  Template CRUD operations (205 lines)
        ├── prompt_builder.py            🎭 Dynamic prompt generation (178 lines)
        └── html_export.py               📄 HTML export & Markdown (369 lines)
```

**Total**: 13 files | ~1,600 lines of code + documentation

---

## 📖 Which Files to Read When

### 🏁 Getting Started (First 10 Minutes)
1. **QUICKSTART.md** - Quick setup and first steps
2. **README.md** - Features overview and installation
3. **requirements.txt** - See what you need to install

### 💻 Using the Application
1. **app.py** - Main application (run this!)
2. **QUICKSTART.md** - Usage examples
3. **README.md** - Detailed usage guide

### 🔨 Customizing & Extending
1. **config/default_templates.json** - See all templates
2. **utils/prompt_builder.py** - Modify perspectives/audiences
3. **utils/template_manager.py** - Understand template system
4. **IMPLEMENTATION_SUMMARY.md** - Extension points

### 🐛 Troubleshooting
1. **TROUBLESHOOTING.md** - Start here for any issues
2. **README.md** - Troubleshooting section
3. **CHANGELOG.md** - What changed from original

### 🏗️ Understanding Architecture
1. **ARCHITECTURE.md** - Visual diagrams and data flow
2. **IMPLEMENTATION_SUMMARY.md** - Design decisions
3. **CHANGELOG.md** - What's new vs original

---

## 🎯 File Details

### Core Application Files

#### `app.py` (468 lines)
**Purpose**: Main Streamlit application with UI and logic flow
**Key Sections**:
- Lines 1-50: Imports and configuration
- Lines 52-108: Helper functions (model fetch, AI response generation)
- Lines 110-162: Session state and navigation
- Lines 164-446: Chat page UI
- Lines 448-587: Template management page UI

**When to Edit**:
- Add new UI elements
- Change page layout
- Modify navigation
- Adjust sidebar organization

#### `requirements.txt` (6 lines)
**Purpose**: Python package dependencies
**Contents**:
```
streamlit>=1.32.0
requests>=2.31.0
langchain-ollama>=0.1.0
langchain-core>=0.1.0
markdown>=3.5.0
```

**When to Edit**:
- Add new Python packages
- Update version requirements
- Lock specific versions for production

### Configuration Files

#### `config/default_templates.json` (30 templates)
**Purpose**: Default question templates (read-only reference)
**Structure**:
```json
{
  "templates": [
    {
      "id": "unique_id",
      "name": "Display Name",
      "template": "Question text",
      "category": "Category",
      "requires_input": true/false,
      "input_label": "Label for input field",
      "description": "What this does"
    }
  ]
}
```

**When to Edit**:
- Add more default templates
- Update existing template descriptions
- Reorganize categories

**Note**: Users shouldn't edit this directly - it's the master copy. Their changes go to `question_templates.json` (auto-created).

### Utility Modules

#### `utils/template_manager.py` (205 lines)
**Purpose**: Manages template CRUD operations and JSON storage
**Key Classes/Functions**:
- `TemplateManager`: Main class
  - `load_templates()`: Read from JSON
  - `save_templates()`: Write to JSON
  - `add_template()`: Create new template
  - `delete_template()`: Remove template
  - `get_template_by_id()`: Retrieve specific template
  - `get_templates_by_category()`: Filter by category
  - `reset_to_defaults()`: Restore original templates

**When to Edit**:
- Change storage format (e.g., to database)
- Add validation logic
- Implement template versioning
- Add template search features

#### `utils/prompt_builder.py` (178 lines)
**Purpose**: Constructs dynamic system prompts based on context
**Key Classes/Functions**:
- `PromptBuilder`: Main class
  - `PERSPECTIVES`: Dictionary of perspective definitions
  - `AUDIENCES`: Dictionary of audience definitions
  - `build_system_prompt()`: Generate contextual prompt
  - `_get_specific_guidance()`: Detailed guidance for combinations

**When to Edit**:
- Add new perspectives (add to `PERSPECTIVES` dict)
- Add new audiences (add to `AUDIENCES` dict)
- Customize guidance for specific combinations
- Change communication style directives

**Example Addition**:
```python
# Add a new perspective
PERSPECTIVES = {
    # ... existing ...
    "Industry Expert": {
        "description": "Professional with real-world experience",
        "style": "practical, solution-oriented, business-focused"
    }
}
```

#### `utils/html_export.py` (369 lines)
**Purpose**: HTML generation and Markdown conversion for exports
**Key Functions**:
- `build_pair_html()`: Single Q&A HTML document
- `build_conversation_html()`: Full conversation HTML
- `_markdown_to_html()`: Markdown to HTML conversion
- `_pipe_table_block_to_html()`: GitHub-style table conversion
- `safe_filename()`: Generate valid filenames

**When to Edit**:
- Change HTML styling (modify Bootstrap classes)
- Adjust export format
- Add PDF export capability
- Customize table rendering

### Documentation Files

#### `README.md` (Comprehensive Guide)
**Sections**:
- Features overview
- Installation instructions
- Usage guide (basic workflow, template management)
- Use cases (scientists, educators, students)
- Customization guide
- Model parameters explained
- Troubleshooting
- Tips & best practices

**For**: Everyone (primary documentation)

#### `QUICKSTART.md` (Quick Guide)
**Sections**:
- 5-minute installation
- 2-minute first steps
- Key features to explore
- Tips for best results
- Common questions

**For**: New users wanting to get started fast

#### `IMPLEMENTATION_SUMMARY.md` (Technical Report)
**Sections**:
- Project overview
- Completed features (detailed)
- Architecture & code organization
- Changes from original code
- Statistics
- Extension points

**For**: Developers wanting technical details

#### `ARCHITECTURE.md` (Visual Guide)
**Sections**:
- Application architecture diagram
- Data flow diagram
- Template system flow
- Component interaction diagrams

**For**: Understanding system design visually

#### `CHANGELOG.md` (Version History)
**Sections**:
- New features (what was added)
- Modified features (what changed)
- Preserved features (what stayed the same)
- Breaking changes (none!)
- Migration guide

**For**: Comparing with original code

#### `TROUBLESHOOTING.md` (Problem Solving)
**Sections**:
- Quick diagnostics checklist
- 10 common issues with solutions
- Advanced troubleshooting
- Platform-specific issues
- Best practices

**For**: When things don't work as expected

---

## 🎓 Development Workflow

### For Scientists (Non-Programmers)

**Just Using the App**:
1. Read: `QUICKSTART.md`
2. Run: `streamlit run app.py`
3. Reference: `README.md` for features
4. If stuck: `TROUBLESHOOTING.md`

**Adding Custom Templates** (No coding required):
1. Run the app
2. Navigate to "Manage Templates"
3. Use "Add Template" tab
4. Fill in the form
5. Save and use immediately

**Customizing Perspectives** (Minimal coding):
1. Open: `utils/prompt_builder.py`
2. Find: `PERSPECTIVES` or `AUDIENCES` dictionary
3. Add your entry following the existing pattern
4. Save and restart app

### For Developers

**Understanding the Code**:
1. Read: `ARCHITECTURE.md` - See system design
2. Read: `IMPLEMENTATION_SUMMARY.md` - Understand decisions
3. Review: `app.py` - Main flow
4. Review: `utils/` files - Business logic

**Making Changes**:
1. **UI Changes**: Edit `app.py`
2. **Template Logic**: Edit `utils/template_manager.py`
3. **Prompt Logic**: Edit `utils/prompt_builder.py`
4. **Export Format**: Edit `utils/html_export.py`
5. **Add Features**: Follow patterns in `app.py`

**Testing Changes**:
```bash
# Run with debug logging
streamlit run app.py --logger.level debug

# Test specific module
python3 -c "from utils.template_manager import TemplateManager; tm = TemplateManager(); print(len(tm.load_templates()))"
```

---

## 💾 Important Files to Backup

### Must Backup (Contains Your Data)
- `config/question_templates.json` - Your custom templates

### Good to Backup (Easy to Restore)
- `config/default_templates.json` - Default templates (rarely changes)
- All `.md` documentation files

### Don't Need to Backup (Generated or Easily Restored)
- `__pycache__/` directories
- `.pyc` files
- Streamlit cache files

**Backup Command**:
```bash
# Backup important files
cp config/question_templates.json config/question_templates_backup_$(date +%Y%m%d).json

# Or backup entire config directory
cp -r config config_backup_$(date +%Y%m%d)
```

---

## 🔍 Quick Reference

### File Size Reference
```
app.py                          ~25 KB
utils/html_export.py           ~19 KB
utils/template_manager.py      ~11 KB
utils/prompt_builder.py        ~10 KB
config/default_templates.json  ~12 KB
README.md                      ~25 KB
IMPLEMENTATION_SUMMARY.md      ~18 KB
ARCHITECTURE.md                ~10 KB
CHANGELOG.md                   ~12 KB
TROUBLESHOOTING.md            ~15 KB
QUICKSTART.md                  ~8 KB
```

### Line Count Reference
```
Python Code:
  app.py:                 468 lines
  template_manager.py:    205 lines
  prompt_builder.py:      178 lines
  html_export.py:         369 lines
  Total Code:           1,220 lines

Documentation:
  All .md files:        ~1,800 lines
  Total Project:        ~3,000 lines
```

---

## 🚀 Next Steps

1. **Read**: `QUICKSTART.md` (5 minutes)
2. **Install**: Follow installation steps (5 minutes)
3. **Run**: `streamlit run app.py`
4. **Explore**: Try different templates and settings
5. **Customize**: Add your own templates
6. **Reference**: Keep `README.md` handy

---

## 🎉 You're All Set!

You have everything you need:
- ✅ Complete working application
- ✅ 30 ready-to-use templates
- ✅ Comprehensive documentation
- ✅ Troubleshooting guide
- ✅ Extension guides
- ✅ Visual architecture diagrams

**Start with**: `QUICKSTART.md`

**Happy exploring! 🔬**
