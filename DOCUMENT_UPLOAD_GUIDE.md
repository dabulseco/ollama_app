# 📄 Document Upload Feature Guide

## Overview

The Local LLM Scientific Assistant now supports **uploading and processing PDF and DOCX documents**. Upload research papers, reports, manuscripts, or any document, and ask questions about them or analyze their content.

---

## Supported File Types

- ✅ **PDF** (.pdf) - Extracts text from all pages
- ✅ **DOCX** (.docx) - Extracts text from paragraphs and tables
- ✅ **DOC** (.doc) - Legacy Word format support

**Maximum file size**: 10 MB per file  
**Multiple files**: Upload multiple documents at once for comparison or combined analysis

---

## How to Use

### Basic Workflow

1. **Navigate to Chat page**
2. **Click "📄 Upload Documents (PDF, DOCX)"** expander
3. **Choose your files** using the file uploader
4. **Click "📥 Process Documents"** to extract text
5. **Ask questions** or use templates with the document content

### Detailed Steps

#### Step 1: Upload Documents

```
1. Click the "📄 Upload Documents" expander section
2. Click "Browse files" or drag-and-drop
3. Select one or more PDF/DOCX files
4. Files appear in the uploader list
```

#### Step 2: Process Documents

```
1. Click the "📥 Process Documents" button
2. Wait for processing (usually 1-10 seconds per file)
3. See success messages with document stats:
   ✅ filename.pdf (2.5 MB, ~5,234 words, 32,145 characters)
```

#### Step 3: Use Document Content

**Option A - Direct Questions:**
```
Type in chat: "What are the main findings of this study?"
The document content is automatically included with your query
```

**Option B - Use Templates:**
```
1. Open "Question Templates" expander
2. Filter to "Document Analysis" category
3. Select template like "Summarize Uploaded Document"
4. Submit - document content included automatically
```

**Option C - Custom Analysis:**
```
Type any question referencing "the document" or "this paper"
Examples:
- "What methodology did they use?"
- "Compare the findings in these papers"
- "What are the limitations mentioned?"
```

---

## Document Management

### View Loaded Documents

After processing, the expander shows:
- ✅ Filename and word count
- 🗑️ Remove button for each document
- 🗑️ Clear All button

### Preview Content

Check the **"👁️ Preview Document Content"** box to see:
- First 2,000 characters of extracted text
- Total character count
- Formatted text with page markers (PDF) or sections (DOCX)

### Remove Documents

**Remove one document:**
- Click 🗑️ next to the filename

**Remove all documents:**
- Click "🗑️ Clear All Documents" button

---

## Document Analysis Templates

The app includes **8 specialized templates** for document work:

### 1. Summarize Uploaded Document
**Purpose**: Get comprehensive summary with key findings  
**Use when**: You want an overview of the entire document

### 2. Extract Key Points from Document
**Purpose**: Bullet-point list of main takeaways  
**Use when**: You need quick reference points

### 3. Analyze Methodology in Document
**Purpose**: Deep dive into research methods  
**Use when**: Evaluating study design and approach

### 4. Compare Multiple Documents
**Purpose**: Side-by-side analysis of uploaded papers  
**Use when**: You uploaded 2+ documents for comparison

### 5. Answer Question from Document
**Purpose**: Specific Q&A about document content  
**Use when**: You have targeted questions

### 6. Create Outline from Document
**Purpose**: Hierarchical structure of document  
**Use when**: You need to understand organization

### 7. Identify Knowledge Gaps
**Purpose**: Find limitations and future research needs  
**Use when**: Planning follow-up research

### 8. Simplify Technical Document
**Purpose**: Translate complex content to accessible language  
**Use when**: Making technical papers understandable

---

## Use Cases

### For Researchers

**Literature Review:**
```
1. Upload 5-10 related papers
2. Use "Compare Multiple Documents" template
3. Get synthesis of findings and methodologies
```

**Paper Analysis:**
```
1. Upload a target paper
2. Use "Analyze Methodology" template
3. Ask follow-up questions about specific sections
```

**Gap Analysis:**
```
1. Upload current state-of-field papers
2. Use "Identify Knowledge Gaps" template
3. Plan your research contribution
```

### For Students

**Study Papers:**
```
1. Upload assigned reading (PDF textbook chapter)
2. Use "Extract Key Points" template
3. Ask questions: "Explain the concept of [X] from this reading"
```

**Essay Research:**
```
1. Upload 3-4 source papers
2. Ask: "What do these sources say about [topic]?"
3. Get synthesized information for your essay
```

### For Educators

**Lesson Planning:**
```
1. Upload research paper on teaching topic
2. Use "Simplify Technical Document" template
3. Get accessible explanations for students
```

**Assignment Creation:**
```
1. Upload source material
2. Ask: "Create 5 discussion questions about this paper"
3. Use for class activities
```

---

## Tips for Best Results

### 📝 Document Preparation

1. **Use text-based PDFs**: Scanned PDFs (images) won't extract well
2. **Check file size**: Keep under 10 MB for faster processing
3. **Clean formatting**: Well-formatted documents extract better
4. **Multiple files**: Upload all related docs together for comparison

### 🎯 Querying Tips

1. **Be specific**: "What methodology is used?" vs "Tell me about this"
2. **Reference sections**: "Summarize the introduction" works well
3. **Multiple docs**: Say "Compare paper 1 and paper 2" or "across all documents"
4. **Follow-up**: Ask clarifying questions in the same conversation

### ⚙️ Performance Tips

1. **Context window**: Large documents may hit token limits
   - Reduce "Context Length" in sidebar if needed
   - Or ask about specific sections
2. **Processing time**: Larger files take longer to read
3. **Multiple queries**: Document stays loaded - ask many questions!

---

## Troubleshooting

### ❌ "Error: PyPDF2 not installed"

**Solution:**
```bash
pip install PyPDF2
```

### ❌ "Error: python-docx not installed"

**Solution:**
```bash
pip install python-docx
```

### ❌ "File too large (15.2 MB). Maximum size is 10 MB"

**Solutions:**
- Split PDF into smaller files
- Compress PDF using online tools
- Extract only relevant pages

### ❌ "No text could be extracted from PDF"

**Causes & Solutions:**
- **Scanned PDF**: Use OCR software first (Adobe Acrobat, online tools)
- **Image-based PDF**: Convert to text-based PDF
- **Encrypted PDF**: Remove password protection first
- **Corrupted file**: Try re-downloading the PDF

### ❌ Garbled or strange characters

**Solutions:**
- Check PDF encoding (should be UTF-8)
- Some PDFs have encoding issues - try different version
- Use "Preview Content" to see what was extracted

### ⚠️ Processing very slow

**Solutions:**
- Reduce document size
- Upload fewer documents at once
- Check file isn't password-protected

---

## Technical Details

### Text Extraction

**PDF Processing:**
- Uses PyPDF2 library
- Extracts text page-by-page
- Preserves page markers: `--- Page 1 ---`
- Handles multi-column layouts (best effort)

**DOCX Processing:**
- Uses python-docx library
- Extracts paragraph text
- Extracts table content with formatting
- Preserves basic structure

### Content Formatting

Documents are formatted as:
```
[Document: filename.pdf]

--- Page 1 ---
[extracted text]

--- Page 2 ---
[extracted text]

=====================================

[Document: another.docx]

[extracted text]
[Table]
header1 | header2
data1   | data2
```

### Integration with Queries

When you submit a query with documents loaded:
```
Your query text

--- UPLOADED DOCUMENT CONTENT ---

[formatted document text]
```

This combined text goes to the LLM, so it has full context.

---

## Limitations

1. **Text-only extraction**: Images, graphs, and equations are not extracted
2. **OCR not included**: Scanned PDFs require pre-processing
3. **Layout preserved minimally**: Complex formatting may be lost
4. **Token limits**: Very large documents may exceed context window
5. **No PDF editing**: Extract text only, cannot modify source files

---

## Advanced Usage

### Batch Processing

```python
# Upload multiple papers at once
# Process all together
# Ask: "Create a comparison table of methodologies across all papers"
```

### Iterative Analysis

```
1. Upload document
2. Get summary (Template: "Summarize Document")
3. Ask follow-up: "Explain the statistical analysis in detail"
4. Ask more: "What are the limitations of this approach?"
5. Finally: "How could this be improved?"
```

### Teaching Applications

```
# Scenario: Explaining complex paper to students
1. Upload research paper (PDF)
2. Set Perspective: "High School Teacher"
3. Set Audience: "High School Student"  
4. Use: "Simplify Technical Document" template
5. Get: Student-appropriate explanation
```

---

## FAQ

**Q: Can I upload images of text?**  
A: No, only text-based PDFs work. Use OCR software first.

**Q: How many documents can I upload?**  
A: No hard limit, but more documents = larger context = slower processing

**Q: Do documents persist between sessions?**  
A: No, documents are session-only. Re-upload after browser refresh.

**Q: Can I edit the extracted text?**  
A: Not directly, but you can copy the preview and paste into your query.

**Q: Does it work with non-English documents?**  
A: Yes, if the PDF/DOCX uses UTF-8 encoding.

**Q: Can I upload .txt files?**  
A: Not currently, but you can copy-paste text directly into queries.

---

## Next Steps

1. ✅ Install document libraries: `pip install PyPDF2 python-docx`
2. ✅ Try uploading a sample PDF
3. ✅ Experiment with document analysis templates
4. ✅ Ask questions about your uploaded documents
5. ✅ Combine with perspective/audience settings for targeted analysis

**Happy analyzing! 📚**
