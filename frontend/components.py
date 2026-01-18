"""
Frontend UI Components Module
File: frontend/components.py
Description: Reusable UI components for the AI PDF Summarizer
"""

import streamlit as st
from datetime import datetime

def render_header():
    """Render premium header"""
    st.markdown("""
    <div class="header-container fade-in">
        <div class="main-title">🚀 AI PDF Summarizer Pro</div>
        <div class="subtitle">Powered by Advanced Large Language Models</div>
        <div class="tagline">Transform lengthy documents into concise insights with cutting-edge AI</div>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render feature highlights"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">Advanced AI Models</div>
            <div class="feature-desc">Llama 2, Mistral, and Phi models for intelligent summarization</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">100% Private</div>
            <div class="feature-desc">All processing happens locally - your data never leaves your device</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Multiple Strategies</div>
            <div class="feature-desc">Choose from 5 different AI-powered summarization approaches</div>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar(ollama):
    """Render premium sidebar"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        st.markdown("### 🔌 Connection Status")
        if ollama.check_connection():
            st.markdown('<div class="status-success">✅ Ollama Connected</div>', unsafe_allow_html=True)
            models = ollama.list_models()
            
            if models:
                st.success(f"📦 {len(models)} model(s) available")
                selected_model = st.selectbox("🤖 Select AI Model", models, help="Choose your AI model")
            else:
                st.warning("⚠️ No models found")
                st.code("ollama pull llama2", language="bash")
                selected_model = st.text_input("Model Name", value="llama2")
        else:
            st.markdown('<div class="status-error">❌ Ollama Not Connected</div>', unsafe_allow_html=True)
            st.error("Start Ollama server:")
            st.code("ollama serve", language="bash")
            st.stop()
        
        st.markdown("---")
        st.markdown("### 📝 Summary Settings")
        
        summary_type = st.radio(
            "Summarization Type",
            [
                "🎯 Extractive (Key Sentences)",
                "✨ Abstractive (AI-Generated)",
                "📌 Bullet Points",
                "❓ Question-Based Analysis",
                "💡 Key Insights"
            ],
            help="Choose how AI should summarize"
        )
        
        summary_length = st.select_slider(
            "📏 Summary Length",
            options=["short", "medium", "long"],
            value="medium",
            help="Control output length"
        )
        
        st.markdown("---")
        st.markdown("### 💾 Quick Actions")
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📚 Help & Info")
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            1. **Upload** your PDF document
            2. **Select** AI model and settings
            3. **Generate** AI-powered summary
            4. **Download** results in TXT or PDF
            """)
        
        with st.expander("🤖 About AI Models"):
            st.markdown("""
            **Llama 2**: Meta's powerful 7B model
            **Mistral**: High-performance European AI
            **Phi**: Microsoft's efficient small model
            """)
        
        return selected_model, summary_type, summary_length

def render_file_info(uploaded_file, total_pages):
    """Render file information cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">📄</div>
            <div class="metric-label">{uploaded_file.name[:20]}...</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{uploaded_file.size / 1024:.1f}</div>
            <div class="metric-label">KB</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_pages}</div>
            <div class="metric-label">Pages</div>
        </div>
        """, unsafe_allow_html=True)

def render_text_statistics(extracted_text):
    """Render text statistics"""
    word_count = len(extracted_text.split())
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">📊 Total Words</div>
            <div class="feature-desc" style="font-size: 1.5rem; font-weight: 600;">{word_count:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">🔤 Characters</div>
            <div class="feature-desc" style="font-size: 1.5rem; font-weight: 600;">{len(extracted_text):,}</div>
        </div>
        """, unsafe_allow_html=True)

def render_processing_status(selected_model, summary_type, summary_length):
    """Render processing status message"""
    st.markdown(f"""
    <div class="status-warning">
        <strong>🤖 Processing with {selected_model}</strong><br>
        Type: {summary_type}<br>
        Length: {summary_length.capitalize()}
    </div>
    """, unsafe_allow_html=True)

def render_summary_statistics(stats, processing_time, selected_model):
    """Render summary statistics cards"""
    st.markdown("## 📊 Summary Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['original_words']:,}</div>
            <div class="metric-label">Original Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['summary_words']:,}</div>
            <div class="metric-label">Summary Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['compression_ratio']:.1f}%</div>
            <div class="metric-label">Compression</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{processing_time:.1f}s</div>
            <div class="metric-label">Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">{selected_model.split(':')[0]}</div>
        </div>
        """, unsafe_allow_html=True)

def render_summary_display(summary, summary_type):
    """Render the summary in styled container"""
    st.markdown("## 📝 AI-Generated Summary")
    st.markdown(f"""
    <div class="summary-container fade-in">
        <div class="summary-header">{summary_type}</div>
        <div class="summary-text">{summary.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

def render_download_section(summary, uploaded_file, summary_type, exporter):
    """Render download buttons"""
    st.markdown("## 💾 Download Your Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download as TXT",
            data=summary,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        pdf_bytes = exporter.create_pdf(summary, uploaded_file.name, summary_type)
        st.download_button(
            label="📑 Download as PDF",
            data=pdf_bytes,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>🎓 AI-Powered PDF Document Summarizer Pro</strong></p>
        <p>Powered by Ollama LLMs | Built with Python & Streamlit</p>
        <p style="font-size: 0.85rem; margin-top: 1rem;">
            Using cutting-edge AI for privacy-preserving document summarization
        </p>
    </div>
    """, unsafe_allow_html=True)
