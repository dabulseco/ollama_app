# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Install Ollama
Visit [ollama.ai](https://ollama.ai) and download the installer for your operating system.

### 2. Install Python Dependencies
```bash
cd ollama_app
pip install -r requirements.txt
```

### 3. Start Ollama and Download a Model
```bash
# In terminal 1: Start Ollama
ollama serve

# In terminal 2: Pull a model (first time only)
ollama pull llama2
```

### 4. Launch the App
```bash
# In terminal 2 (or a new terminal)
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

## First Steps (2 minutes)

### 1. Configure Context (Left Sidebar)
- **Perspective**: Choose "Scientist" (who's writing)
- **Audience**: Choose "College Student" (who's reading)
- **Model**: Select "llama2" (or whichever model you downloaded)

### 2. Try a Template
1. Click **"📋 Question Templates"** (main page)
2. Select category: **"Teaching"**
3. Choose: **"Explain Scientific Concept"**
4. Click **"📝 Use Template with Form"**
5. Enter a concept like: "photosynthesis"
6. Click **"🚀 Submit Question"**

### 3. Try Free-Form Chat
Just type in the chat input: "Explain how CRISPR works"

## Key Features to Explore

### ✅ Change Who's Talking
Try different combinations:
- **Scientist → High School Student**: Technical but accessible
- **Teacher → Middle School Student**: Very clear, age-appropriate
- **Lay Person → Scientist**: Informal but detailed

### ✅ Browse All Templates
Navigate to **"Manage Templates"** (left sidebar) to see all 30+ templates organized by:
- Research (papers, methods, critique)
- Teaching (lessons, analogies, experiments)
- Laboratory (protocols, safety, troubleshooting)
- Statistics (tests, interpretation)
- And more!

### ✅ Create Your Own Template
1. Go to **"Manage Templates"** → **"➕ Add Template"**
2. Fill in:
   - Name: "Explain Like I'm Five"
   - Category: "Custom"
   - Template: "Explain this concept in the simplest possible terms:"
   - Check "Requires user input"
3. Click **"➕ Add Template"**
4. Use it immediately from the Chat page!

### ✅ Export Your Work
- After any conversation, click **"⬇️ Download Full Conversation"**
- Get professional HTML with Bootstrap styling
- Perfect for sharing or keeping records

## Tips for Best Results

### 🎯 For Teaching
- **Perspective**: "High School Teacher"
- **Audience**: Match your students' level
- **Templates**: Use "Create Analogy" and "Design Experiment"

### 🎯 For Research
- **Perspective**: "Scientist"
- **Audience**: "Scientist" or "College Student"
- **Templates**: Use "Summarize Research Paper" and "Critique Study"

### 🎯 For Lab Work
- **Perspective**: "Scientist"
- **Audience**: Match your team's expertise
- **Templates**: Use "Design Laboratory Protocol" and "Troubleshoot Experiment"

## Common Questions

**Q: Can I change perspective mid-conversation?**  
A: The current version applies perspective/audience to the entire conversation. To switch, start a new conversation (click "Clear History").

**Q: Where are my templates saved?**  
A: In `config/question_templates.json` - you can backup this file!

**Q: Can I use this offline?**  
A: Yes! Everything runs locally. No internet needed after installation.

**Q: Which model should I use?**  
A: Start with `llama2` (good balance of speed and quality). Try `mistral` for coding questions.

**Q: Why are responses slow?**  
A: Try reducing "Context Length" in sidebar settings, or use a smaller model variant (e.g., `llama2:7b`).

## Next Steps

1. ✅ Explore all template categories
2. ✅ Create 2-3 custom templates for your common questions
3. ✅ Try different perspective/audience combinations
4. ✅ Experiment with model parameters
5. ✅ Export and save your important conversations

## Need Help?

- 📖 Full documentation: See `README.md`
- 🐛 Troubleshooting: Check the Troubleshooting section in README
- 💡 Model parameters: See "Model Parameters Explained" in README

**Happy exploring! 🔬**
