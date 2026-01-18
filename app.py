"""
AI-Powered PDF Document Summarizer - Main Application
File: app.py
Author: Academic Project
Description: Modern, professional UI with clean architecture
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

# Import backend modules
from backend import (
    ollama_client as OllamaClient,
    pdf_extractor as PDFTextExtractor,
    summarizer as AISummarizer,
    exporter as SummaryExporter,
    utils as calculate_statistics
)

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
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application with premium UI"""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize Ollama client
    ollama = OllamaClient.OllamaClient()
    
    # Render header
    render_header()
    
    # Render features
    render_features()
    
    # Render sidebar and get settings
    selected_model, summary_type, summary_length = render_sidebar(ollama)
    
    st.markdown("---")
    
    # Main content area
    st.markdown("## 📁 Upload Your PDF Document")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your PDF document for AI-powered summarization"
    )
    
    if uploaded_file:
        # Extract text from PDF
        with st.spinner("📖 Extracting text from PDF..."):
            extractor = PDFTextExtractor.PDFTextExtractor()
            extracted_text, total_pages = extractor.extract_text_from_pdf(uploaded_file)
        
        # Render file information
        render_file_info(uploaded_file, total_pages)
        
        if extracted_text:
            # Show text preview in expander
            with st.expander("📄 View Extracted Text Preview"):
                st.text_area(
                    "",
                    extracted_text[:2000] + "...",
                    height=300,
                    disabled=True
                )
            
            # Render text statistics
            render_text_statistics(extracted_text)
            
            st.markdown("---")
            
            # Generate summary button
            if st.button(
                "🚀 Generate AI Summary",
                type="primary",
                use_container_width=True
            ):
                # Initialize summarizer
                summarizer = AISummarizer.AISummarizer(ollama)
                
                # Show processing status
                with st.container():
                    render_processing_status(
                        selected_model,
                        summary_type,
                        summary_length
                    )
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                
                start_time = time.time()
                
                try:
                    # Update progress
                    status_text.text("🔄 Sending to AI model...")
                    progress_bar.progress(25)
                    
                    # Generate summary based on selected type
                    if "Extractive" in summary_type:
                        summary = summarizer.summarize_extractive(
                            extracted_text,
                            selected_model,
                            summary_length
                        )
                    elif "Abstractive" in summary_type:
                        summary = summarizer.summarize_abstractive(
                            extracted_text,
                            selected_model,
                            summary_length
                        )
                    elif "Bullet" in summary_type:
                        summary = summarizer.summarize_bullet_points(
                            extracted_text,
                            selected_model
                        )
                    elif "Question" in summary_type:
                        summary = summarizer.summarize_with_questions(
                            extracted_text,
                            selected_model
                        )
                    else:  # Key Insights
                        summary = summarizer.get_key_insights(
                            extracted_text,
                            selected_model
                        )
                    
                    # Update progress
                    progress_bar.progress(75)
                    status_text.text("⚙️ Processing response...")
                    
                    if summary:
                        # Complete progress
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Calculate processing time and statistics
                        processing_time = time.time() - start_time
                        stats = calculate_statistics.calculate_statistics(extracted_text, summary)
                        
                        # Success message
                        st.markdown(
                            f"""
                            <div class="status-success">
                                ✅ Summary Generated Successfully in {processing_time:.1f} seconds!
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        st.markdown("---")
                        
                        # Render summary statistics
                        render_summary_statistics(
                            stats,
                            processing_time,
                            selected_model
                        )
                        
                        st.markdown("---")
                        
                        # Display summary
                        render_summary_display(summary, summary_type)
                        
                        # Copy-friendly text area
                        with st.expander("📋 Copy-Friendly Text"):
                            st.text_area("", summary, height=300)
                        
                        st.markdown("---")
                        
                        # Download section
                        exporter = SummaryExporter.SummaryExporter()
                        render_download_section(
                            summary,
                            uploaded_file,
                            summary_type,
                            exporter
                        )
                        
                        # Model information footer
                        st.markdown("---")
                        st.info(
                            f"🤖 Generated using **{selected_model}** | "
                            f"📅 {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
                        )
                    
                    else:
                        # Failed to generate summary
                        progress_bar.empty()
                        status_text.empty()
                        st.markdown(
                            '<div class="status-error">❌ Failed to generate summary</div>',
                            unsafe_allow_html=True
                        )
                        st.info("💡 Try a different model or shorter document")
                
                except Exception as e:
                    # Handle errors
                    progress_bar.empty()
                    status_text.empty()
                    st.markdown(
                        f'<div class="status-error">❌ Error: {str(e)}</div>',
                        unsafe_allow_html=True
                    )
                    st.info("💡 Check your Ollama connection and try again")
        
        else:
            # Could not extract text
            st.markdown(
                '<div class="status-error">❌ Could not extract text from PDF</div>',
                unsafe_allow_html=True
            )
            st.info(
                "💡 Ensure your PDF contains readable text (not scanned images)"
            )
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
