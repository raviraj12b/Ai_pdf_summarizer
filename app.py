"""
AI-Powered PDF Document Summarizer - Premium UI
File: app.py
Author: Academic Project
Description: Modern, professional UI with advanced features
"""

import streamlit as st
import PyPDF2
import requests
import json
import time
from fpdf import FPDF
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import frontend modules
from frontend import (
    load_custom_css,
    render_header,
    render_features,
    render_sidebar,
    render_file_info,
    render_text_statistics,
    render_processing_status,
    render_summary_statistics,
    render_summary_display,
    render_download_section,
    render_footer
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI PDF Summarizer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# BACKEND CLASSES
# ============================================================================

class OllamaClient:
    """Client for Ollama API"""
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.models_url = f"{base_url}/api/tags"
    
    def check_connection(self):
        try:
            response = requests.get(self.models_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        try:
            response = requests.get(self.models_url, timeout=5)
            if response.status_code == 200:
                return [model['name'] for model in response.json().get('models', [])]
            return []
        except:
            return []
    
    def generate(self, model, prompt, stream=False):
        try:
            payload = {"model": model, "prompt": prompt, "stream": stream}
            response = requests.post(self.generate_url, json=payload, timeout=300)
            if response.status_code == 200:
                return response.json()['response']
            return None
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return None

class PDFTextExtractor:
    """PDF text extraction"""
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            total_pages = len(pdf_reader.pages)
            
            progress_bar = st.progress(0)
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
                progress_bar.progress((page_num + 1) / total_pages)
            
            progress_bar.empty()
            return text, total_pages
        except Exception as e:
            st.error(f"Extraction error: {str(e)}")
            return None, 0

class AISummarizer:
    """AI-powered summarization"""
    def __init__(self, ollama_client):
        self.ollama = ollama_client
    
    def summarize_abstractive(self, text, model, length="medium"):
        length_map = {
            "short": "3-4 sentences",
            "medium": "5-7 sentences",
            "long": "8-12 sentences"
        }
        
        prompt = f"""You are an expert at abstractive text summarization.

TEXT TO SUMMARIZE:
{text[:8000]}

Write a {length_map[length]} summary in your own words.
Focus on main ideas and key points.

SUMMARY:"""
        return self.ollama.generate(model, prompt)
    
    def summarize_extractive(self, text, model, length="medium"):
        length_map = {
            "short": "3-4 key sentences",
            "medium": "5-7 key sentences",
            "long": "8-12 key sentences"
        }
        
        prompt = f"""You are an expert at extractive summarization.

TEXT:
{text[:8000]}

Select {length_map[length]} from the original text that capture the main ideas.

SUMMARY:"""
        return self.ollama.generate(model, prompt)
    
    def summarize_bullet_points(self, text, model):
        prompt = f"""Create 5-8 bullet points summarizing this text.

TEXT:
{text[:8000]}

BULLET POINTS:"""
        return self.ollama.generate(model, prompt)
    
    def summarize_with_questions(self, text, model):
        prompt = f"""Analyze this text by answering:
1. Main topic?
2. Key findings?
3. Evidence provided?
4. Conclusions?

TEXT:
{text[:8000]}

ANALYSIS:"""
        return self.ollama.generate(model, prompt)
    
    def get_key_insights(self, text, model):
        prompt = f"""Extract key insights from this text.

TEXT:
{text[:8000]}

Provide:
1. Top 3-5 insights
2. Main takeaways
3. Implications

INSIGHTS:"""
        return self.ollama.generate(model, prompt)

class SummaryExporter:
    """Export summaries"""
    @staticmethod
    def create_pdf(summary_text, title="Summary", summary_type=""):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AI-Generated Summary", ln=True, align='C')
        pdf.ln(5)
        
        if summary_type:
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(0, 10, f"Type: {summary_type}", ln=True, align='C')
            pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, title, ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", size=11)
        for line in summary_text.split('\n'):
            if line.strip():
                pdf.multi_cell(0, 8, line.encode('latin-1', 'replace').decode('latin-1'))
        
        return pdf.output(dest='S').encode('latin-1')

def calculate_statistics(original, summary):
    """Calculate summary statistics"""
    orig_words = len(original.split())
    summ_words = len(summary.split())
    compression = ((orig_words - summ_words) / orig_words) * 100 if orig_words > 0 else 0
    return {
        'original_words': orig_words,
        'summary_words': summ_words,
        'compression_ratio': compression
    }

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application with premium UI"""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize Ollama
    ollama = OllamaClient()
    
    # Render header
    render_header()
    
    # Render features
    render_features()
    
    # Render sidebar and get settings
    selected_model, summary_type, summary_length = render_sidebar(ollama)
    
    st.markdown("---")
    
    # Main content area
    st.markdown("## 📂 Upload Your PDF Document")
   
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your PDF document for AI-powered summarization"
    )
    
    if uploaded_file:
        # Extract text
        with st.spinner("📖 Extracting text from PDF..."):
            extractor = PDFTextExtractor()
            extracted_text, total_pages = extractor.extract_text_from_pdf(uploaded_file)
        
        # Render file info
        render_file_info(uploaded_file, total_pages)
        
        if extracted_text:
            # Text preview
            with st.expander("📄 View Extracted Text Preview"):
                st.text_area("", extracted_text[:2000] + "...", height=300, disabled=True)
            
            # Statistics
            render_text_statistics(extracted_text)
            
            st.markdown("---")
            
            # Generate button
            if st.button("🚀 Generate AI Summary", type="primary", use_container_width=True):
                summarizer = AISummarizer(ollama)
                
                # Progress container
                with st.container():
                    render_processing_status(selected_model, summary_type, summary_length)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                
                start_time = time.time()
                
                try:
                    status_text.text("🔄 Sending to AI model...")
                    progress_bar.progress(25)
                    
                    # Generate based on type
                    if "Extractive" in summary_type:
                        summary = summarizer.summarize_extractive(extracted_text, selected_model, summary_length)
                    elif "Abstractive" in summary_type:
                        summary = summarizer.summarize_abstractive(extracted_text, selected_model, summary_length)
                    elif "Bullet" in summary_type:
                        summary = summarizer.summarize_bullet_points(extracted_text, selected_model)
                    elif "Question" in summary_type:
                        summary = summarizer.summarize_with_questions(extracted_text, selected_model)
                    else:
                        summary = summarizer.get_key_insights(extracted_text, selected_model)
                    
                    progress_bar.progress(75)
                    status_text.text("⚙️ Processing response...")
                    
                    if summary:
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        progress_bar.empty()
                        status_text.empty()
                        
                        processing_time = time.time() - start_time
                        stats = calculate_statistics(extracted_text, summary)
                        
                        # Success message
                        st.markdown(f"""
                        <div class="status-success">
                            ✅ Summary Generated Successfully in {processing_time:.1f} seconds!
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # Render statistics
                        render_summary_statistics(stats, processing_time, selected_model)
                        
                        st.markdown("---")
                        
                        # Display summary
                        render_summary_display(summary, summary_type)
                        
                        # Copy-friendly version
                        with st.expander("📋 Copy-Friendly Text"):
                            st.text_area("", summary, height=300)
                        
                        st.markdown("---")
                        
                        # Download section
                        exporter = SummaryExporter()
                        render_download_section(summary, uploaded_file, summary_type, exporter)
                        
                        # Model info
                        st.markdown("---")
                        st.info(f"🤖 Generated using **{selected_model}** | 📅 {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
                    
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.markdown('<div class="status-error">❌ Failed to generate summary</div>', unsafe_allow_html=True)
                        st.info("💡 Try a different model or shorter document")
                
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.markdown(f'<div class="status-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ Could not extract text from PDF</div>', unsafe_allow_html=True)
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()
