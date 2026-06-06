import os
import streamlit as st
from dotenv import load_dotenv
from document_processor import process_document

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="NyayaRedline AI | Smart Contract Review",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = None
if 'audit_results' not in st.session_state:
    st.session_state['audit_results'] = None
if 'audit_started' not in st.session_state:
    st.session_state['audit_started'] = False

# Sidebar Configuration
with st.sidebar:
    st.header("Control Panel")
    st.subheader("System Status")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        st.success("Google GenAI: Connected (v2.5)")
    else:
        st.error("Google GenAI: Missing Key")
        
    sarvam_key = os.getenv("SARVAM_API_KEY")
    if sarvam_key:
        st.success("Sarvam AI REST: Connected")
    else:
        st.error("Sarvam AI REST: Missing Key")
        
    st.markdown("---")
    # Tying the toggle directly to Phase 2 Fallback Mechanism
    demo_mode = st.toggle("Enable Offline Demo Mode (Fallback Data)", value=False)
    st.markdown("---")
    st.caption("NyayaRedline AI Framework")

# Main Application Interface
st.title("NyayaRedline AI")
st.subheader("Smart Contract Review and Redlining Tool for MSMEs")
st.markdown("---")

# Two Column Layout
col1, col2 = st.columns([1, 1], gap="large")

# Left Column: Document Ingestion
with col1:
    st.header("1. Document Input")
    st.markdown("Upload a legal contract or agreement PDF to begin processing")
    
    uploaded_file = st.file_uploader("Select Contract File", type=["pdf"])
    
    if uploaded_file is not None or demo_mode:
        
        if demo_mode:
            st.warning("Demo Mode Active: Using fallback contract data")
            st.session_state['extracted_text'] = process_document(b"", use_fallback=True)
        elif uploaded_file is not None:
            st.success(f"Loaded: {uploaded_file.name}")
            if st.session_state['extracted_text'] is None:
                with st.spinner("Extracting text and analyzing layout"):
                    file_bytes = uploaded_file.read()
                    st.session_state['extracted_text'] = process_document(file_bytes, use_fallback=False)
        
        st.markdown("### Extracted Content View")
        st.text_area(
            "Raw Text (Read-Only)", 
            value=st.session_state['extracted_text'], 
            height=400, 
            disabled=True
        )
        
        if st.button("Run Legal Audit", type="primary", use_container_width=True):
            st.session_state['audit_started'] = True
    else:
        st.info("Awaiting document upload")
        st.session_state['extracted_text'] = None
        st.session_state['audit_started'] = False

# Right Column: Analysis and Output
with col2:
    st.header("2. Legal Analysis and Redlines")
    
    if st.session_state['audit_started'] and st.session_state['extracted_text']:
        st.warning("Executing statutory analysis engine")
        
        st.markdown("### Identified Violations and Risk Scores")
        st.info("Core Intelligence evaluation cards will populate this space in Phase 3")
        
        st.markdown("### Regional Language Localization")
        st.info("Sarvam AI audio player and translation elements will render here in Phase 4")
    else:
        st.markdown(
            "Once you upload a contract and click Run Legal Audit, "
            "the analysis, statutory risks, and multi-lingual playbacks will display here"
        )