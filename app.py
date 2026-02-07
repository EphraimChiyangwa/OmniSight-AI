"""
OmniSight-AI: High-Performance Enterprise Dashboard
Refactored for Centralized Navigation and Modular Views.
"""

import streamlit as st
import os
import ai_engine as ai_engine
import data_generator as data_generator
# Import the new view modules
from views import dashboard, predictive, scenario, deepdive

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="OmniSight AI | Enterprise Intelligence",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Slate-Gray Aesthetic & Custom Navigation Styling
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #4c525a; color: #ffffff; }
    
    /* Hide standard Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---- CUSTOM NAVIGATION BAR STYLING ---- */
    div[role="radiogroup"] {
        flex-direction: row;
        justify-content: center;
        background: #2c313a;
        padding: 10px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 25px;
    }
    div[role="radio"] {
        background: transparent;
        margin: 0 5px;
        padding: 8px 20px;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    div[role="radio"]:hover {
         background: rgba(255,255,255,0.05);
    }
    div[role="radio"][aria-checked="true"] {
        background: rgba(0, 242, 234, 0.15) !important;
        border-color: rgba(0, 242, 234, 0.5) !important;
        color: #00f2ea !important;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0, 242, 234, 0.2);
    }
    div[role="radio"] > div:first-child { display: none; }
    div[role="radio"] > div:last-child { margin-left: 0px; }

    /* Metric Cards */
    .metric-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.05);
        text-align: left;
    }
    .metric-val { font-size: 28px; font-weight: 700; color: white; margin: 5px 0; }
    .metric-lbl { font-size: 13px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; }
    .metric-delta { font-size: 12px; font-weight: bold; }
    .delta-pos { color: #48bb78; } 
    .delta-neg { color: #f56565; }

    /* Analysis Box */
    .analysis-container {
        background: #1a202c;
        border-left: 4px solid #00f2ea;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: #2d3748;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #00f2ea;
        color: #00f2ea;
        background: rgba(0, 242, 234, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA & STATE MANAGEMENT ---
@st.cache_data(ttl=300)
def load_data():
    return {
        "finance": data_generator.get_financial_data(),
        "operations": data_generator.get_operations_data(),
        "partners": data_generator.get_partner_data(),
        "clients": data_generator.get_client_data(),
        "competitive": data_generator.get_competitive_data(),
        "compliance": data_generator.get_compliance_data()
    }

if 'state_data' not in st.session_state:
    st.session_state.state_data = load_data()
if 'ai_analysis' not in st.session_state: st.session_state.ai_analysis = None
if 'prediction' not in st.session_state: st.session_state.prediction = None
if 'scenario_result' not in st.session_state: st.session_state.scenario_result = None

current_data = st.session_state.state_data

# --- 3. HEADER & NAVIGATION ---
header_c1, header_c2 = st.columns([3, 1])
with header_c1:
    # UPDATED LOGO PATH HERE (OmniSightLogo.png)
    logo_path = os.path.join("image", "OmniSightLogo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.markdown("## 👁️ OmniSight AI")

with header_c2:
    if st.button("🔄 Refresh Data Stream", use_container_width=True):
        st.cache_data.clear()
        st.session_state.state_data = load_data()
        st.session_state.ai_analysis = None
        st.session_state.prediction = None
        st.session_state.scenario_result = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

selected_view = st.radio(
    "Navigation",
    ["Dashboard", "Predictive Analytics", "Scenario Modeling", "Domain Deep Dive"],
    label_visibility="collapsed",
    horizontal=True
)

# --- 4. MAIN CONTENT ROUTING ---
if selected_view == "Dashboard":
    dashboard.show(current_data, ai_engine)
elif selected_view == "Predictive Analytics":
    predictive.show(current_data, ai_engine)
elif selected_view == "Scenario Modeling":
    scenario.show(current_data, ai_engine)
elif selected_view == "Domain Deep Dive":
    deepdive.show(current_data, ai_engine)

st.markdown("<br><br><center><small style='color: #a0aec0'>OmniSight AI v2.2 | Real-Time Enterprise Agent | Status: <span style='color:#48bb78'>● Online</span></small></center>", unsafe_allow_html=True)