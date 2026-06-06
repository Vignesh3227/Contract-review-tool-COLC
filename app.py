import os
import streamlit as st
from dotenv import load_dotenv


from document_processor import process_document, FALLBACK_CONTRACT_TEXT
from audit_engine import run_contract_audit
from redline_engine import create_dummy_pdf, generate_redlined_pdf
from sarvam_service import translate_text, text_to_speech


load_dotenv()


st.set_page_config(
    page_title="NyayaRedline AI | Smart Contract Review",
    layout="wide",
    initial_sidebar_state="expanded"
)


LANGUAGES = {
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Tamil": "ta-IN",
    "Marathi": "mr-IN"
}


if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = None
if 'audit_results' not in st.session_state:
    st.session_state['audit_results'] = None
if 'audit_started' not in st.session_state:
    st.session_state['audit_started'] = False
if 'original_pdf_bytes' not in st.session_state:
    st.session_state['original_pdf_bytes'] = None
if 'redlined_pdf_bytes' not in st.session_state:
    st.session_state['redlined_pdf_bytes'] = None
if 'audio_cache' not in st.session_state:
    st.session_state['audio_cache'] = {}


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
   
    demo_mode = st.toggle("Enable Offline Demo Mode (Fallback Data)", value=False)
    st.markdown("---")
    st.caption("NyayaRedline AI Framework - Built for Indian MSMEs")


st.title("NyayaRedline AI")
st.subheader("Smart Contract Review and Redlining Tool for MSMEs")
st.markdown("---")


col1, col2 = st.columns([1, 1], gap="large")


with col1:
    st.header("1. Document Input")
    st.markdown("Upload a legal contract (PDF or Image) to begin processing")
    
    uploaded_file = st.file_uploader("Select Contract File", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None or demo_mode:
        
        
        if demo_mode:
            st.warning("Demo Mode Active: Using fallback contract data")
            st.session_state['extracted_text'] = process_document(b"", file_name="", use_fallback=True)
            st.session_state['original_pdf_bytes'] = create_dummy_pdf(FALLBACK_CONTRACT_TEXT)
            
      
        elif uploaded_file is not None:
            st.success(f"Loaded: {uploaded_file.name}")
            
            
            if 'current_file' not in st.session_state or st.session_state['current_file'] != uploaded_file.name:
                st.session_state['extracted_text'] = None
                st.session_state['audit_results'] = None
                st.session_state['redlined_pdf_bytes'] = None
                st.session_state['audio_cache'] = {}
                st.session_state['current_file'] = uploaded_file.name
                st.session_state['audit_started'] = False
                
           
            if st.session_state['extracted_text'] is None:
                with st.spinner("Extracting text and analyzing layout..."):
                    file_bytes = uploaded_file.read()
                    st.session_state['original_pdf_bytes'] = file_bytes
                    st.session_state['extracted_text'] = process_document(
                        file_bytes, 
                        file_name=uploaded_file.name, 
                        use_fallback=False
                    )
        
        
        st.markdown("### Extracted Content View")
        st.text_area(
            "Raw Text (Read-Only)", 
            value=st.session_state['extracted_text'], 
            height=350, 
            disabled=True
        )
        
        
        if st.button("Run Legal Audit", type="primary", use_container_width=True):
            st.session_state['audit_started'] = True
            st.session_state['audit_results'] = None
            st.session_state['redlined_pdf_bytes'] = None
            st.session_state['audio_cache'] = {}
    else:
        st.info("Awaiting document upload")
        for key in ['extracted_text', 'audit_results', 'original_pdf_bytes', 'redlined_pdf_bytes']:
            st.session_state[key] = None
        st.session_state['audio_cache'] = {}
        st.session_state['audit_started'] = False
        if 'current_file' in st.session_state:
            del st.session_state['current_file']



with col2:
    st.header("2. Legal Analysis and Redlines")
    
    if st.session_state['audit_started'] and st.session_state['extracted_text']:
        
        
        if st.session_state['audit_results'] is None:
            with st.spinner("Analyzing legal parameters against Indian statutory frameworks..."):
                st.session_state['audit_results'] = run_contract_audit(st.session_state['extracted_text'])
                
        results = st.session_state['audit_results']
        
        if "error" in results:
            st.error(results["error"])
        else:
          
            risk_score = results.get("overall_risk_score", 0)
            
            
            if risk_score > 70:
                st.error(f"Overall Contract Risk Index: {risk_score} / 100")
            elif risk_score > 40:
                st.warning(f"Overall Contract Risk Index: {risk_score} / 100")
            else:
                st.success(f"Overall Contract Risk Index: {risk_score} / 100")
                
            st.info(f"**Executive Summary:** {results.get('summary', '')}")
            st.markdown("---")
            
            
            if st.session_state['redlined_pdf_bytes'] is None and st.session_state['original_pdf_bytes']:
                with st.spinner("Generating visual redlines and injecting legal annotations..."):
                    st.session_state['redlined_pdf_bytes'] = generate_redlined_pdf(
                        st.session_state['original_pdf_bytes'], 
                        results
                    )
            
            
            if st.session_state['redlined_pdf_bytes']:
                st.download_button(
                    label="📄 Download Redlined Contract (PDF)",
                    data=st.session_state['redlined_pdf_bytes'],
                    file_name="NyayaRedline_Audited_Contract.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            st.markdown("---")
            
            
            st.markdown("### Identified Vulnerabilities")
            issues = results.get("issues", [])
            
            if not issues:
                st.success("No high-risk vulnerabilities identified in this contract.")
                
            for idx, issue in enumerate(issues):
                with st.container(border=True):
                    severity = issue.get("severity", "Low")
                    
                    if severity == "High":
                        st.error(f"🚨 High Risk: {issue.get('clause_title')}")
                    elif severity == "Medium":
                        st.warning(f"⚠️ Medium Risk: {issue.get('clause_title')}")
                    else:
                        st.info(f"ℹ️ Low Risk: {issue.get('clause_title')}")
                        
                    st.markdown(f"**Governing Law:** {issue.get('governing_act')}")
                    st.write(issue.get("description"))
                    st.markdown(f"**Suggested Revision:**\n`{issue.get('recommended_redline')}`")
                    
                    st.markdown("---")
                    
                    st.markdown("#### 🎧 Regional Voice Explainer")
                    
                    lang_col, btn_col = st.columns([1, 2])
                    with lang_col:
                        selected_lang_name = st.selectbox(
                            "Language", 
                            options=list(LANGUAGES.keys()), 
                            key=f"lang_sel_{idx}",
                            label_visibility="collapsed"
                        )
                    
                    target_lang_code = LANGUAGES[selected_lang_name]
                    cache_key = f"audio_{idx}_{target_lang_code}"
                    
                    with btn_col:
                        if st.button(f"Generate Audio Explanation", key=f"btn_{idx}", use_container_width=True):
                            with st.spinner(f"Translating and generating {selected_lang_name} audio..."):
                                translated_text = translate_text(issue.get("description"), target_lang=target_lang_code)
                                audio_bytes = text_to_speech(translated_text, target_lang=target_lang_code)
                                
                                if audio_bytes:
                                    st.session_state['audio_cache'][cache_key] = audio_bytes
                                else:
                                    st.error("Failed to generate audio. Check API connections.")
                                    
                    
                    if cache_key in st.session_state['audio_cache']:
                        st.success(f"Audio ready in {selected_lang_name}")
                        st.audio(st.session_state['audio_cache'][cache_key], format="audio/wav")
                        
           
            safe_clauses = results.get("safe_clauses", [])
            if safe_clauses:
                st.markdown("### Validated Clauses")
                with st.expander("View Approved and Compliant Sections"):
                    for safe in safe_clauses:
                        st.success(f"**✅ {safe.get('clause_title')}**")
                        st.write(safe.get('reasoning'))
                        st.markdown("---")

    else:
        st.markdown(
            "Once you upload a contract and click **Run Legal Audit**, "
            "the analysis, statutory risks, and multi-lingual playbacks will display here."
        )