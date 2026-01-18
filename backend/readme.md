# Backend Module Documentation

## Overview

The `backend` folder contains all the core logic for the AI-Powered PDF Summarizer, separated from the frontend UI code for clean architecture and maintainability.

---

## 📁 File Structure

```
backend/
├── __init__.py           # Package initialization
├── ollama_client.py      # Ollama API communication
├── pdf_extractor.py      # PDF text extraction
├── summarizer.py         # AI summarization logic
├── exporter.py           # Summary export functions
├── utils.py              # Utility functions
└── README.md             # This file
```

---

## 📚 Modules

### 1. `ollama_client.py`

**Purpose**: Handles all communication with Ollama API

**Main Class**: `OllamaClient`

**Key Methods**:
- `check_connection()` - Verify Ollama server is running
- `list_models()` - Get available AI models
- `generate(model, prompt)` - Generate text using LLM
- `chat(model, messages)` - Chat-based interaction
- `get_model_info(model)` - Get model details

**Usage Example**:
```python
from backend import OllamaClient

ollama = OllamaClient()
if ollama.check_connection():
    models = ollama.list_models()
    response = ollama.generate("llama2", "Summarize this text...")
```

---

### 2. `pdf_extractor.py`

**Purpose**: Extract text from PDF documents

**Main Class**: `PDFTextExtractor`

**Key Methods**:
- `extract_text_from_pdf(pdf_file)` - Extract all text
- `validate_pdf(pdf_file)` - Check if PDF is valid
- `get_pdf_metadata(pdf_file)` - Get PDF info
- `extract_text_by_page(pdf_file, page_num)` - Extract specific page

**Usage Example**:
```python
from backend import PDFTextExtractor

extractor = PDFTextExtractor()
text, pages = extractor.extract_text_from_pdf(uploaded_file)
```

---

### 3. `summarizer.py`

**Purpose**: AI-powered text summarization with multiple strategies

**Main Class**: `AISummarizer`

**Key Methods**:
- `summarize_extractive(text, model, length)` - Select key sentences
- `summarize_abstractive(text, model, length)` - Generate new summary
- `summarize_bullet_points(text, model)` - Create bullet list
- `summarize_with_questions(text, model)` - Question-based analysis
- `get_key_insights(text, model)` - Extract insights
- `custom_summarize(text, model, prompt)` - Custom instructions

**Usage Example**:
```python
from backend import AISummarizer, OllamaClient

ollama = OllamaClient()
summarizer = AISummarizer(ollama)

# Abstractive summary
summary = summarizer.summarize_abstractive(
    text,
    model="llama2",
    length="medium"
)

# Bullet points
bullets = summarizer.summarize_bullet_points(text, "mistral")
```

---

### 4. `exporter.py`

**Purpose**: Export summaries to various formats

**Main Class**: `SummaryExporter`

**Key Methods**:
- `create_pdf(summary, title, type, metadata)` - Create PDF file
- `create_txt(summary, title, type, metadata)` - Create text file
- `create_markdown(summary, title, type, metadata)` - Create Markdown

**Usage Example**:
```python
from backend import SummaryExporter

exporter = SummaryExporter()

# Create PDF
pdf_bytes = exporter.create_pdf(
    summary_text,
    title="My Document",
    summary_type="Abstractive",
    metadata={
        'model': 'llama2',
        'date': '2024-01-20',
        'compression': 95.5
    }
)

# Create formatted text
txt_content = exporter.create_txt(summary_text, "My Document")
```

---

### 5. `utils.py`

**Purpose**: Helper functions and utilities

**Key Functions**:
- `calculate_statistics(original, summary)` - Get word counts, compression
- `validate_text_length(text, max_length)` - Check and truncate
- `estimate_processing_time(words, model)` - Estimate duration
- `clean_text(text)` - Normalize text
- `split_into_chunks(text, size, overlap)` - Split long documents
- `format_time(seconds)` - Format time display
- `get_file_size_mb(file)` - Get file size
- `truncate_filename(name, max_len)` - Shorten filenames
- `count_sentences(text)` - Count sentences
- `get_reading_time(text)` - Estimate reading time
- `extract_key_stats(text)` - Get comprehensive stats

**Usage Example**:
```python
from backend import calculate_statistics, format_time

# Get statistics
stats = calculate_statistics(original_text, summary_text)
print(f"Compression: {stats['compression_ratio']:.1f}%")

# Format time
formatted = format_time(125.5)  # "2.1m"
```

---

## 🚀 Quick Start

### Installation

```bash
# Install required packages
pip install PyPDF2 requests fpdf
```

### Basic Usage

```python
# Import all backend components
from backend import (
    OllamaClient,
    PDFTextExtractor,
    AISummarizer,
    SummaryExporter,
    calculate_statistics
)

# 1. Initialize Ollama
ollama = OllamaClient()

# 2. Extract PDF text
extractor = PDFTextExtractor()
text, pages = extractor.extract_text_from_pdf(pdf_file)

# 3. Summarize
summarizer = AISummarizer(ollama)
summary = summarizer.summarize_abstractive(text, "llama2", "medium")

# 4. Get statistics
stats = calculate_statistics(text, summary)

# 5. Export
exporter = SummaryExporter()
pdf_bytes = exporter.create_pdf(summary, "My Summary")
```

---

## 🔧 Configuration

### Ollama Connection

Default: `http://localhost:11434`

To change:
```python
ollama = OllamaClient(base_url="http://your-server:11434")
```

### Context Window Limits

Default: 8000 characters (in summarizer.py)

To modify, edit the `[:8000]` slice in summarizer.py prompts.

---

## 🧪 Testing

### Test Ollama Connection

```python
from backend import OllamaClient

ollama = OllamaClient()
if ollama.check_connection():
    print("✅ Ollama connected")
    print(f"Models: {ollama.list_models()}")
else:
    print("❌ Ollama not running")
```

### Test PDF Extraction

```python
from backend import PDFTextExtractor

extractor = PDFTextExtractor()

# Validate PDF
if extractor.validate_pdf(pdf_file):
    text, pages = extractor.extract_text_from_pdf(pdf_file)
    print(f"Extracted {len(text)} characters from {pages} pages")
```

### Test Summarization

```python
from backend import OllamaClient, AISummarizer

ollama = OllamaClient()
summarizer = AISummarizer(ollama)

test_text = "Your test document text here..."
summary = summarizer.summarize_abstractive(test_text, "llama2")
print(f"Summary: {summary}")
```

---

## 🐛 Error Handling

All modules include comprehensive error handling:

```python
try:
    text, pages = extractor.extract_text_from_pdf(pdf_file)
except Exception as e:
    print(f"Error: {e}")
```

Common errors are caught and displayed with helpful messages via Streamlit's `st.error()`.

---

## 📊 Performance

### Processing Times (Approximate)

| Document Size | Llama 2 | Mistral | Phi |
|--------------|---------|---------|-----|
| 1K words | 8s | 6s | 4s |
| 5K words | 25s | 18s | 12s |
| 10K words | 45s | 32s | 22s |

### Memory Usage

- **Minimum RAM**: 8GB (for 7B models)
- **Recommended RAM**: 16GB
- **Model Sizes** (quantized):
  - Phi: 1.6GB
  - Llama 2: 3.8GB
  - Mistral: 4.1GB

---

## 🔄 Extending the Backend

### Adding a New Summarization Strategy

1. Add method to `AISummarizer` class in `summarizer.py`:

```python
def summarize_custom(self, text, model):
    """Your custom summarization strategy"""
    prompt = f"""Your custom prompt here...
    
    TEXT:
    {text[:8000]}
    
    SUMMARY:"""
    return self.ollama.generate(model, prompt)
```

2. Use in app.py:

```python
summary = summarizer.summarize_custom(text, model)
```

### Adding a New Export Format

1. Add method to `SummaryExporter` class in `exporter.py`:

```python
@staticmethod
def create_json(summary_text, metadata):
    """Export as JSON"""
    import json
    data = {
        'summary': summary_text,
        'metadata': metadata
    }
    return json.dumps(data, indent=2)
```

### Adding Utility Functions

1. Add to `utils.py`:

```python
def your_utility_function(arg1, arg2):
    """Your utility function description"""
    # Implementation
    return result
```

2. Export in `__init__.py`:

```python
from .utils import your_utility_function

__all__ = [
    # ... existing exports
    'your_utility_function'
]
```

---

## 📝 API Reference

### OllamaClient

```python
class OllamaClient:
    def __init__(self, base_url="http://localhost:11434")
    def check_connection() -> bool
    def list_models() -> list
    def generate(model: str, prompt: str, stream: bool = False) -> str
    def chat(model: str, messages: list, stream: bool = False) -> str
    def get_model_info(model_name: str) -> dict
```

### PDFTextExtractor

```python
class PDFTextExtractor:
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> tuple[str, int]
    @staticmethod
    def validate_pdf(pdf_file) -> bool
    @staticmethod
    def get_pdf_metadata(pdf_file) -> dict
    @staticmethod
    def extract_text_by_page(pdf_file, page_number: int) -> str
```

### AISummarizer

```python
class AISummarizer:
    def __init__(self, ollama_client: OllamaClient)
    def summarize_extractive(text: str, model: str, length: str) -> str
    def summarize_abstractive(text: str, model: str, length: str) -> str
    def summarize_bullet_points(text: str, model: str) -> str
    def summarize_with_questions(text: str, model: str) -> str
    def get_key_insights(text: str, model: str) -> str
    def custom_summarize(text: str, model: str, custom_prompt: str) -> str
```

### SummaryExporter

```python
class SummaryExporter:
    @staticmethod
    def create_pdf(summary: str, title: str, type: str, metadata: dict) -> bytes
    @staticmethod
    def create_txt(summary: str, title: str, type: str, metadata: dict) -> str
    @staticmethod
    def create_markdown(summary: str, title: str, type: str, metadata: dict) -> str
```

---

## 🤝 Contributing

To contribute to the backend:

1. Ensure code follows existing patterns
2. Add docstrings to all functions
3. Include error handling
4. Test thoroughly
5. Update this README

---

## 📄 License

Same as main project - MIT License

---

## 🔗 Dependencies

```
PyPDF2==3.0.1      # PDF processing
requests==2.31.0   # HTTP requests
fpdf==1.7.2        # PDF generation
```

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
