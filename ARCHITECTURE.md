# Application Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LOCAL LLM SCIENTIFIC ASSISTANT                    │
│                              (Streamlit App)                             │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
          ┌─────────▼─────────┐          ┌──────────▼──────────┐
          │   CHAT PAGE       │          │  TEMPLATE MGMT PAGE │
          │                   │          │                     │
          │ - Chat Input      │          │ - View Templates    │
          │ - Template Browse │          │ - Add Template      │
          │ - History Display │          │ - Delete Template   │
          │ - Export Buttons  │          │ - Reset to Defaults │
          └─────────┬─────────┘          └──────────┬──────────┘
                    │                               │
                    └────────────┬──────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   SIDEBAR CONTROLS      │
                    │                         │
                    │ - Navigation            │
                    │ - Perspective Select    │
                    │ - Audience Select       │
                    │ - Model Settings        │
                    │ - Parameters Sliders    │
                    │ - Question History      │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐    ┌─────────▼──────────┐   ┌────────▼─────────┐
│ PROMPT BUILDER │    │ TEMPLATE MANAGER   │   │   HTML EXPORT    │
│                │    │                    │   │                  │
│ - Build System │    │ - Load Templates   │   │ - Markdown→HTML  │
│   Prompts      │    │ - Save Templates   │   │ - Bootstrap Style│
│ - Perspective  │    │ - Add Template     │   │ - Export Convo   │
│   Definitions  │    │ - Delete Template  │   │ - Export Q&A     │
│ - Audience     │    │ - Get by Category  │   │                  │
│   Definitions  │    │                    │   │                  │
└────────────────┘    └─────────┬──────────┘   └──────────────────┘
                                │
                      ┌─────────▼──────────┐
                      │   JSON STORAGE     │
                      │                    │
                      │ default_templates  │
                      │ question_templates │
                      └────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL DEPENDENCIES                           │
└─────────────────────────────────────────────────────────────────────────┘
        │                        │                         │
┌───────▼────────┐    ┌─────────▼──────────┐    ┌────────▼─────────┐
│    OLLAMA      │    │    LANGCHAIN       │    │   STREAMLIT      │
│                │    │                    │    │                  │
│ - Local LLM    │    │ - ChatOllama       │    │ - UI Framework   │
│ - Model Serve  │    │ - Prompt Templates │    │ - Session State  │
│ - API Endpoint │    │ - Output Parser    │    │ - Components     │
└────────────────┘    └────────────────────┘    └──────────────────┘
```

## Data Flow Diagram

```
USER INPUT
    │
    ├─ [Direct Chat Input] ──────────────────────┐
    │                                             │
    └─ [Template Selection] ─┐                   │
                              │                   │
        [Select Template]     │                   │
              │               │                   │
              ▼               │                   │
        ┌──────────────┐      │                   │
        │ Form Mode?   │      │                   │
        └──────┬───────┘      │                   │
               │              │                   │
        ┌──────┴──────┐       │                   │
        │             │       │                   │
    [Yes]         [No]        │                   │
        │             │       │                   │
        ▼             ▼       │                   │
    [Fill Form]   [Populate]  │                   │
        │         Chat Input   │                   │
        │             │        │                   │
        └─────────────┴────────┘                   │
                  │                                │
                  ▼                                │
            [User Query] ◄───────────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  Build Context   │
        │  - Perspective   │
        │  - Audience      │
        │  - Chat History  │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Generate Prompt  │
        │ with PromptBuild │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Send to LLM     │
        │  (via Ollama)    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Receive Response│
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Store in History │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Display + Export │
        └──────────────────┘
```

## Template System Flow

```
┌─────────────────────────────────────────────────────┐
│               TEMPLATE LIFECYCLE                     │
└─────────────────────────────────────────────────────┘

[Application Start]
        │
        ▼
┌──────────────────┐
│ Load Default     │
│ Templates?       │
└────────┬─────────┘
         │
    [First Run]
         │
         ▼
┌──────────────────┐      ┌──────────────────────┐
│ Copy Defaults to │─────▶│ question_templates   │
│ User Templates   │      │ .json created        │
└──────────────────┘      └──────────────────────┘
         │
         │
         ▼
┌──────────────────────────────────────────────┐
│        TEMPLATE OPERATIONS                   │
├──────────────────────────────────────────────┤
│                                              │
│  [View] ──▶ Load → Filter → Display         │
│                                              │
│  [Add]  ──▶ Form → Validate → Save          │
│                                              │
│  [Delete]─▶ Confirm → Remove → Save         │
│                                              │
│  [Use]  ──▶ Select → Mode? ──┬──▶ Form      │
│                               └──▶ Chat      │
│                                              │
│  [Reset]──▶ Confirm → Restore Defaults      │
│                                              │
└──────────────────────────────────────────────┘
```

## Key Components Interaction

```
┌──────────────┐
│   USER       │
└──────┬───────┘
       │
       │ Interacts with
       ▼
┌──────────────┐       Uses        ┌──────────────┐
│  STREAMLIT   │◄───────────────────│    UTILS     │
│     UI       │                    │              │
└──────┬───────┘                    │ - Templates  │
       │                            │ - Prompts    │
       │ Calls                      │ - HTML       │
       ▼                            └──────────────┘
┌──────────────┐
│  LANGCHAIN   │
│   WRAPPER    │
└──────┬───────┘
       │
       │ Sends Prompt
       ▼
┌──────────────┐
│   OLLAMA     │
│   API        │
└──────┬───────┘
       │
       │ Returns Response
       ▼
┌──────────────┐
│   DISPLAY    │
│   & EXPORT   │
└──────────────┘
```
