import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables on startup
load_dotenv()

# Configure the Streamlit page layout
st.set_page_config(
    page_title="NyayaRedline AI | Smart Contract Review",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Configuration
with st.sidebar:
    st.header("Control Panel")
    
    st.subheader("System Status")
    gemini_status = "Connected" if os.getenv("GEMINI_API_KEY") else "Missing Key"
    sarvam_status = "Connected" if os.getenv("SARVAM_API_KEY") else "Missing Key"
    
    st.text(f"Gemini AI Engine: {gemini_status}")
    st.text(f"Sarvam AI Engine: {sarvam_status}")
    
    st.markdown("---")
    st.subheader("Hackathon Settings")
    demo_mode = st.toggle("Enable Offline Demo Mode", value=False, help="Bypass API calls and use cached data for live judging.")
    
    st.markdown("---")
    st.caption("Developed by Team Cease and Desist")
    st.caption("The Code of Law Challenge")

# Main Application Header
st.title("NyayaRedline AI")
st.subheader("Smart Contract Review & Redlining Tool for MSMEs")

# Establish the two-column workspace
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("1. Document Input")
    st.markdown("Upload a legal contract (PDF or Image) to begin the audit.")
    
    uploaded_file = st.file_uploader("Select Contract File", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.success(f"File loaded: {uploaded_file.name}")
        
        # Placeholder for the document preview or text extraction display
        with st.expander("View Document Preview", expanded=True):
            st.info("Document rendering and OCR extraction pipeline will be integrated here in Phase 2.")
            
        if st.button("Run Legal Audit", type="primary", use_container_width=True):
            st.session_state['audit_started'] = True
    else:
        st.info("Awaiting document upload...")

with col2:
    st.header("2. Legal Analysis & Redlines")
    
    if 'audit_started' in st.session_state and st.session_state['audit_started']:
        st.warning("Executing Statutory Audit... (Placeholder)")
        
        # Placeholder for the Toxicity Gauge
        st.metric(label="Contract Bias Score", value="Pending API", delta="Calculating...", delta_color="inverse")
        
        # Placeholder for the interactive redline UI and voice explainer
        st.markdown("### Identified Issues")
        st.info("The JSON parsing logic and Sarvam TTS integration will render individual clause analyses here in Phase 3.")
        
        # Placeholder for the final PDF download
        st.markdown("### Generate Clean File")
        st.download_button(
            label="Download Redlined PDF",
            data=b"Placeholder data",
            file_name="nyayaredline_audit.pdf",
            mime="application/pdf",
            disabled=True,
            use_container_width=True
        )
    else:
        st.markdown("Upload a document and initialize the audit to view statutory violations, suggested replacements, and the final redlined contract.")