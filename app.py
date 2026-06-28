# import sys
# import os
# import importlib.util
# import pandas as pd
# import streamlit as st
# from pathlib import Path
# import time
# from datetime import datetime

# ROOT = Path(__file__).resolve().parent


# def _configure_hf_token() -> None:
#     try:
#         token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGINGFACE_HUB_TOKEN")
#     except Exception:
#         token = None

#     if token:
#         token = str(token).strip()
#         os.environ["HF_TOKEN"] = token
#         os.environ["HUGGINGFACE_HUB_TOKEN"] = token


# _configure_hf_token()

# # Import your native main automation function from redrob-ranker/rank.py
# rank_path = ROOT / "redrob-ranker" / "rank.py"
# spec = importlib.util.spec_from_file_location("redrob_rank", str(rank_path))
# rank_module = importlib.util.module_from_spec(spec)
# if spec.loader is not None:
#     spec.loader.exec_module(rank_module)
# else:
#     raise ImportError(f"Could not load rank module from {rank_path}")
# run_pipeline = rank_module.main

# # ============================================================================
# # PAGE CONFIGURATION
# # ============================================================================
# st.set_page_config(
#     page_title="Redrob AI - Candidate Ranking",
#     page_icon="🎯",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ============================================================================
# # CUSTOM CSS & STYLING
# # ============================================================================
# st.markdown("""
# <style>
#     /* Global Styling */
#     * {
#         margin: 0;
#         padding: 0;
#     }
    
#     /* Main Container */
#     .main {
#         padding-top: 0rem;
#     }
    
#     /* Header Styling */
#     .header-container {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem 2rem;
#         border-radius: 15px;
#         margin-bottom: 2rem;
#         box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
#     }
    
#     .header-title {
#         font-size: 2.5rem;
#         font-weight: 800;
#         color: white;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 2px 10px rgba(0,0,0,0.2);
#     }
    
#     .header-subtitle {
#         font-size: 1.1rem;
#         color: rgba(255,255,255,0.9);
#     }
    
#     /* Input Section */
#     .input-section {
#         background: white;
#         padding: 2rem;
#         border-radius: 12px;
#         border-left: 5px solid #667eea;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.08);
#         margin-bottom: 2rem;
#     }
    
#     .input-label {
#         font-size: 1.1rem;
#         font-weight: 600;
#         color: #333;
#         margin-bottom: 0.8rem;
#     }
    
#     /* Button Styling */
#     .stButton > button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         padding: 1rem 2rem;
#         border-radius: 10px;
#         font-size: 1.1rem;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
#     }
    
#     .stButton > button:active {
#         transform: translateY(0px);
#     }
    
#     /* Results Section */
#     .results-section {
#         background: white;
#         padding: 2rem;
#         border-radius: 12px;
#         border-top: 5px solid #667eea;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.08);
#     }
    
#     /* Info Box */
#     .info-box {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         border-left: 4px solid #667eea;
#         margin: 1rem 0;
#         color: #333;
#     }
    
#     /* Success Message */
#     .success-message {
#         background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         color: white;
#         font-weight: 600;
#         margin: 1rem 0;
#     }
    
#     /* Error Message */
#     .error-message {
#         background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         color: white;
#         font-weight: 600;
#         margin: 1rem 0;
#     }
    
#     /* Data Table */
#     .dataframe {
#         border-radius: 10px !important;
#         overflow: hidden;
#     }
    
#     /* Loading Spinner */
#     .stSpinner {
#         color: #667eea;
#     }
    
#     /* Download Button */
#     .stDownloadButton > button {
#         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         color: white;
#         border: none;
#         padding: 0.8rem 1.5rem;
#         border-radius: 8px;
#         font-size: 1rem;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
#     }
    
#     .stDownloadButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5);
#     }
    
#     /* Text Input */
#     .stTextInput > div > div > input {
#         border-radius: 8px;
#         border: 2px solid #e0e0e0;
#         padding: 0.8rem;
#         transition: all 0.3s ease;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#     }
    
#     /* File Uploader */
#     .stFileUploader {
#         border-radius: 10px;
#     }
    
#     /* Metric Cards */
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 1px solid #e0e0e0;
#         text-align: center;
#         transition: all 0.3s ease;
#     }
    
#     .metric-card:hover {
#         box-shadow: 0 8px 20px rgba(0,0,0,0.1);
#         transform: translateY(-3px);
#     }
    
#     .metric-value {
#         font-size: 2rem;
#         font-weight: 800;
#         color: #667eea;
#     }
    
#     .metric-label {
#         font-size: 0.9rem;
#         color: #666;
#         margin-top: 0.5rem;
#     }
    
#     /* Progress Bar */
#     .progress-bar {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         height: 8px;
#         border-radius: 10px;
#         margin: 1rem 0;
#     }
    
#     /* Divider */
#     hr {
#         border: none;
#         height: 2px;
#         background: linear-gradient(90deg, transparent, #667eea, transparent);
#         margin: 2rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================================
# # HEADER SECTION
# # ============================================================================
# st.markdown("""
# <div class="header-container">
#     <div class="header-title">🎯 Redrob AI</div>
#     <div class="header-subtitle">Advanced Candidate Ranking & Evaluation Engine</div>
# </div>
# """, unsafe_allow_html=True)

# ROOT = Path(__file__).resolve().parent

# # ============================================================================
# # MAIN CONTENT AREA
# # ============================================================================
# st.markdown("### 📋 Input Configuration")

# # Create two columns for better spacing
# col1, col2 = st.columns([1, 0.05])

# with col1:
#     st.markdown("""
#     <div class="input-section">
#     """, unsafe_allow_html=True)
    
#     # File uploader
#     st.markdown('<p class="input-label">📄 Upload Candidates Data</p>', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader(
#         "Select JSONL file",
#         type=["jsonl"],
#         label_visibility="collapsed",
#         help="📌 Drag & drop or browse your candidates.jsonl file"
#     )
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Output filename
#     st.markdown('<p class="input-label">📊 Output File Name</p>', unsafe_allow_html=True)
#     output_filename = st.text_input(
#         "File name",
#         value="top_100_candidates.csv",
#         label_visibility="collapsed",
#         placeholder="e.g., ranked_candidates.csv"
#     )
    
#     st.markdown("""
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# # ============================================================================
# # ACTION BUTTON
# # ============================================================================
# col_button = st.columns([1, 1, 1])
# with col_button[1]:
#     execute_pipeline = st.button(
#         "🚀 Evaluate & Rank Candidates",
#         use_container_width=True,
#         key="execute_btn"
#     )

# st.markdown("<br>", unsafe_allow_html=True)

# # ============================================================================
# # PIPELINE EXECUTION
# # ============================================================================
# if execute_pipeline:
#     if uploaded_file is None:
#         progress_placeholder = st.empty()
#         status_placeholder = st.empty()
        
#         with progress_placeholder.container():
#             progress_bar = st.progress(0)
#             status_text = st.empty()
        
#         try:
            
#             # Step 2: Prepare pipeline
#             status_text.markdown("⏳ Preparing pipeline arguments...")
#             progress_bar.progress(40)
#             time.sleep(0.3)
            
#             pipeline_args = [
#                 "rank.py",
#                 "--skip-stage1"
#             ]
            
#             # Step 3: Initialize execution
#             status_text.markdown("⏳ Initializing ranking engine...")
#             progress_bar.progress(60)
#             time.sleep(0.3)
            
#             # Step 4: Run pipeline
#             status_text.markdown("⏳ Running candidate evaluation & ranking (this may take a moment)...")
#             progress_bar.progress(80)
            
#             sys.argv = pipeline_args
#             run_pipeline()
            
#             # Step 5: Complete
#             status_text.markdown("⏳ Finalizing results...")
#             progress_bar.progress(100)
#             time.sleep(0.5)
            
#             # Clear progress and show success
#             progress_placeholder.empty()
#             st.markdown("""
#             <div class="success-message">
#             ✅ Pipeline completed successfully! Rankings generated for top 100 candidates.
#             </div>
#             """, unsafe_allow_html=True)
            
#             st.balloons()
            
#         except Exception as error:
#             progress_placeholder.empty()
#             st.markdown(f"""
#             <div class="error-message">
#             ❌ Error occurred: {str(error)}
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         upload_dir = ROOT / "static"
#         upload_dir.mkdir(exist_ok=True)
#         # Paths
#         final_out_path = str(ROOT / "static" /output_filename)
#         temp_jsonl_path = str(ROOT / "static"/ uploaded_file.name)
        
#         # Create progress placeholder
#         progress_placeholder = st.empty()
#         status_placeholder = st.empty()
        
#         with progress_placeholder.container():
#             progress_bar = st.progress(0)
#             status_text = st.empty()
        
#         try:
#             # Step 1: Save uploaded file
#             status_text.markdown("⏳ Uploading candidates data...")
#             progress_bar.progress(20)
#             time.sleep(0.3)
            
#             with open(temp_jsonl_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             # Step 2: Prepare pipeline
#             status_text.markdown("⏳ Preparing pipeline arguments...")
#             progress_bar.progress(40)
#             time.sleep(0.3)
            
#             pipeline_args = [
#                 "rank.py",
#                 "--candidates", temp_jsonl_path,
#                 "--out", final_out_path,
#                 "--skip-stage1"
#             ]
            
#             # Step 3: Initialize execution
#             status_text.markdown("⏳ Initializing ranking engine...")
#             progress_bar.progress(60)
#             time.sleep(0.3)
            
#             # Step 4: Run pipeline
#             status_text.markdown("⏳ Running candidate evaluation & ranking (this may take a moment)...")
#             progress_bar.progress(80)
            
#             sys.argv = pipeline_args
#             run_pipeline()
            
#             # Step 5: Complete
#             status_text.markdown("⏳ Finalizing results...")
#             progress_bar.progress(100)
#             time.sleep(0.5)
            
#             # Clear progress and show success
#             progress_placeholder.empty()
#             st.markdown("""
#             <div class="success-message">
#             ✅ Pipeline completed successfully! Rankings generated for top 100 candidates.
#             </div>
#             """, unsafe_allow_html=True)
            
#             st.balloons()
            
#         except Exception as error:
#             progress_placeholder.empty()
#             st.markdown(f"""
#             <div class="error-message">
#             ❌ Error occurred: {str(error)}
#             </div>
#             """, unsafe_allow_html=True)


# st.markdown("<br>", unsafe_allow_html=True)

# # ============================================================================
# # RESULTS DISPLAY SECTION
# # ============================================================================
# st.markdown("### 📊 Results & Rankings")
# final_out_path = str(ROOT / "static" /output_filename)
# if output_filename is None:
#     final_out_path =  str(ROOT / "submission.csv")
# if os.path.exists(final_out_path):
#     try:
#         df = pd.read_csv(final_out_path)
        
#         # Keep only top 100
#         if len(df) > 100:
#             df = df.head(100)
        
#         # Metrics row
#         metric_col1, metric_col2, metric_col3 = st.columns(3)
        
#         with metric_col1:
#             st.markdown("""
#             <div class="metric-card">
#                 <div class="metric-value">✨</div>
#                 <div class="metric-label">Total Candidates</div>
#                 <div class="metric-value" style="font-size: 1.8rem;">""" + str(len(df)) + """</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with metric_col2:
#             if len(df) > 0:
#                 avg_score = df['score'].mean()
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-value">📈</div>
#                     <div class="metric-label">Average Score</div>
#                     <div class="metric-value" style="font-size: 1.8rem;">{avg_score:.2f}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
        
#         with metric_col3:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-value">🏆</div>
#                 <div class="metric-label">Top Ranked</div>
#                 <div class="metric-value" style="font-size: 1.8rem;">#{df.iloc[0]['rank']}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # Data table
#         st.markdown("#### 🎯 Top Ranked Candidates")
        
#         # Format dataframe for display
#         display_df = df[["candidate_id", "rank", "score", "reasoning"]].copy()
#         display_df['score'] = display_df['score'].apply(lambda x: f"{x:.4f}")
        
#         st.dataframe(
#             display_df.head(100),
#             use_container_width=True,
#             height=400,
#             hide_index=True
#         )
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # Download button
#         with open(final_out_path, "rb") as file:
#             st.download_button(
#                 label="📥 Download CSV",
#                 data=file,
#                 file_name=output_filename,
#                 mime="text/csv",
#                 use_container_width=True
#             )
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # Additional info
#         st.markdown("#### 📈 Dataset Information")
#         col_info1, col_info2 = st.columns(2)
        
#         with col_info1:
#             st.info(f"""
#             **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
#             **File:** {output_filename}
#             """)
        
#         with col_info2:
#             st.info(f"""
#             **Records:** {len(df)} candidates
            
#             **Status:** ✅ Ready for download
#             """)
            
#     except Exception as e:
#         st.markdown(f"""
#         <div class="error-message">
#         ⚠️ Could not display results: {str(e)}
#         </div>
#         """, unsafe_allow_html=True)
# else:
#     st.markdown("""
#     <div class="info-box">
#     👆 Run the pipeline above to generate and display results here
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================================
# # FOOTER
# # ============================================================================
# st.markdown("<br><br>", unsafe_allow_html=True)
# st.markdown("""
# ---
# <div style="text-align: center; color: #999; font-size: 0.9rem;">
#     <p>🚀 Redrob AI Ranking Engine | Powered by Advanced ML Models</p>
#     <p>© 2026 India Runs Team - Code Crusaders</p>
# </div>
# """, unsafe_allow_html=True)


import sys
import os
import importlib.util
import pandas as pd
import streamlit as st
from pathlib import Path
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parent


def _configure_hf_token() -> None:
    try:
        token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGINGFACE_HUB_TOKEN")
    except Exception:
        token = None

    if token:
        token = str(token).strip()
        os.environ["HF_TOKEN"] = token
        os.environ["HUGGINGFACE_HUB_TOKEN"] = token


_configure_hf_token()

# Import your native main automation function from redrob-ranker/rank.py
rank_path = ROOT / "redrob-ranker" / "rank.py"
spec = importlib.util.spec_from_file_location("redrob_rank", str(rank_path))
rank_module = importlib.util.module_from_spec(spec)
if spec.loader is not None:
    spec.loader.exec_module(rank_module)
else:
    raise ImportError(f"Could not load rank module from {rank_path}")
run_pipeline = rank_module.main

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Redrob AI - Candidate Ranking",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS & STYLING (Optimized for Dark Theme)
# ============================================================================
st.markdown("""
<style>
    /* Global Styling Override */
    * {
        margin: 0;
        padding: 0;
    }
    
    /* Main Container */
    .main {
        padding-top: 0rem;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
    }
    
    /* Input Section (Adapted for Dark Theme Visibility) */
    .input-section {
        background: #1e1e24;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    }
    
    .input-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.8rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        color: white;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Results Section */
    .results-section {
        background: #1e1e24;
        padding: 2rem;
        border-radius: 12px;
        border-top: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #2c2c35 0%, #1e1e24 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #e0e0e0;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Error Message */
    .error-message {
        background: linear-gradient(135deg, #c62828 0%, #b71c1c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Data Table */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
    }
    
    /* Loading Spinner */
    .stSpinner {
        color: #667eea;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5);
        color: white;
    }
    
    /* Text Input Alignment */
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #1e1e24;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #33333f;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b0b0b0;
        margin-top: 0.5rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================
st.markdown("""
<div class="header-container">
    <div class="header-title">🎯 Redrob AI</div>
    <div class="header-subtitle">Advanced Candidate Ranking & Evaluation Engine</div>
</div>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
st.markdown("### 📋 Input Configuration")

st.markdown('<div class="input-section">', unsafe_allow_html=True)

# File uploader - Single file only
st.markdown('<p class="input-label">📄 Upload Candidates Data</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Select JSONL file",
    type=["jsonl"],
    label_visibility="collapsed",
    accept_multiple_files=False
)

st.markdown("<br>", unsafe_allow_html=True)

# Output filename
st.markdown('<p class="input-label">📊 Output File Name</p>', unsafe_allow_html=True)
output_filename = st.text_input(
    "File name",
    value="top_100_candidates.csv",
    label_visibility="collapsed",
    placeholder="e.g., ranked_candidates.csv"
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# ACTION BUTTON
# ============================================================================
col_button = st.columns([1, 1, 1])
with col_button[1]:
    execute_pipeline = st.button(
        "🚀 Evaluate & Rank Candidates",
        use_container_width=True,
        key="execute_btn"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# PIPELINE EXECUTION
# ============================================================================
if execute_pipeline:
    if uploaded_file is None:
        st.markdown("""
        <div class="error-message">
        ⚠️ Please upload a candidates JSONL file before evaluating.
        </div>
        """, unsafe_allow_html=True)
    else:
        upload_dir = ROOT / "static"
        upload_dir.mkdir(exist_ok=True)
        
        final_out_path = str(ROOT / "static" / output_filename)
        temp_jsonl_path = str(ROOT / "static" / uploaded_file.name)
        
        progress_placeholder = st.empty()
        
        with progress_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        try:
            status_text.markdown("⏳ Uploading candidates data...")
            progress_bar.progress(20)
            time.sleep(0.3)
            
            with open(temp_jsonl_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            status_text.markdown("⏳ Preparing pipeline arguments...")
            progress_bar.progress(40)
            time.sleep(0.3)
            
            pipeline_args = [
                "rank.py",
                "--candidates", temp_jsonl_path,
                "--out", final_out_path,
                "--skip-stage1"
            ]
            
            status_text.markdown("⏳ Initializing ranking engine...")
            progress_bar.progress(60)
            time.sleep(0.3)
            
            status_text.markdown("⏳ Running candidate evaluation & ranking (this may take a moment)...")
            progress_bar.progress(80)
            
            sys.argv = pipeline_args
            run_pipeline()
            
            status_text.markdown("⏳ Finalizing results...")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            progress_placeholder.empty()
            st.markdown("""
            <div class="success-message">
            ✅ Pipeline completed successfully! Rankings generated for top 100 candidates.
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
        except Exception as error:
            progress_placeholder.empty()
            st.markdown(f"""
            <div class="error-message">
            ❌ Error occurred: {str(error)}
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# RESULTS DISPLAY SECTION
# ============================================================================
st.markdown("### 📊 Results & Rankings")
final_out_path = str(ROOT / "static" / output_filename)
if output_filename is None:
    final_out_path = str(ROOT / "submission.csv")

if os.path.exists(final_out_path):
    try:
        df = pd.read_csv(final_out_path)
        
        if len(df) > 100:
            df = df.head(100)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">✨</div>
                <div class="metric-label">Total Candidates</div>
                <div class="metric-value" style="font-size: 1.8rem;">""" + str(len(df)) + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            if len(df) > 0:
                avg_score = df['score'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">📈</div>
                    <div class="metric-label">Average Score</div>
                    <div class="metric-value" style="font-size: 1.8rem;">{avg_score:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🏆</div>
                <div class="metric-label">Top Ranked</div>
                <div class="metric-value" style="font-size: 1.8rem;">#{df.iloc[0]['rank'] if 'rank' in df.columns else 1}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("#### 🎯 Top Ranked Candidates")
        
        cols_to_display = [col for col in ["candidate_id", "rank", "score", "reasoning"] if col in df.columns]
        display_df = df[cols_to_display].copy()
        if 'score' in display_df.columns:
            display_df['score'] = display_df['score'].apply(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)
        
        st.dataframe(
            display_df.head(100),
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with open(final_out_path, "rb") as file:
            st.download_button(
                label="📥 Download CSV",
                data=file,
                file_name=output_filename,
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("#### 📈 Dataset Information")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.info(f"""
            **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            **File:** {output_filename}
            """)
        
        with col_info2:
            st.info(f"""
            **Records:** {len(df)} candidates
            
            **Status:** ✅ Ready for download
            """)
            
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
        ⚠️ Could not display results: {str(e)}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
    👆 Run the pipeline above to generate and display results here
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
---
<div style="text-align: center; color: #999; font-size: 0.9rem;">
    <p>🚀 Redrob AI Ranking Engine | Powered by Advanced ML Models</p>
    <p>© 2026 India Runs Team - Code Crusaders</p>
</div>
""", unsafe_allow_html=True)