import streamlit as st
import pandas as pd
import numpy as np
import time
from openai import OpenAI

# --- CUSTOM MODULES ---
import ai_engine       # The Brain
import data_generator  # The Data Source

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="OmniSight AI | Enterprise Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    div[data-testid="stSidebar"] { background-color: #2e1a47; }
    div[data-testid="stSidebar"] * { color: white !important; }
    .stMetricValue { color: #6f42c1 !important; font-weight: bold; }
    .stAlert { background-color: #f3f0f7; border: 1px solid #dcd3e9; color: #2e1a47; }
    h1, h2, h3 { color: #2e1a47 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING FUNCTION ---
def refresh_data():
    raw_fin = data_generator.get_financial_data()
    raw_ops = data_generator.get_operations_data()
    raw_partners = data_generator.get_partner_data()
    
    try:
        raw_clients = data_generator.get_client_data()
    except AttributeError:
        raw_clients = []

    full_state = {
        "finance": raw_fin,
        "operations": raw_ops,
        "partners": raw_partners,
        "clients": raw_clients
    }
    
    total_revenue = sum(item['amount'] for item in raw_fin if item['type'] == 'Income')
    active_ops = sum(1 for item in raw_ops if item['status'] == 'Active')
    reliable_partners = sum(1 for item in raw_partners if item.get('reliability') == 'High')

    return full_state, total_revenue, active_ops, reliable_partners

# --- 3. SESSION STATE INITIALIZATION ---
if 'state_data' not in st.session_state:
    data, rev, ops, partners = refresh_data()
    st.session_state.state_data = data
    st.session_state.metric_revenue = rev
    st.session_state.metric_ops = ops
    st.session_state.metric_partners = partners
    st.session_state.briefing = "🔵 **System Ready.** Click 'Run AI Analysis' to generate an intelligence report."

# --- 4. UI LAYOUT ---
st.title("🌐 OmniSight AI")
st.markdown("**Real-Time Enterprise Intelligence System**")
st.divider()

col1, col2, col3 = st.columns([1, 1.5, 1])

# COLUMN 1: LIVE STATUS
with col1:
    st.subheader("📡 Domain Status")
    with st.expander("💰 Financial Health", expanded=True):
        st.metric("Total Revenue", f"${st.session_state.metric_revenue:,.0f}", "+5.2%")
    with st.expander("⚙️ Operations", expanded=True):
        st.metric("Active Lines", st.session_state.metric_ops)
    with st.expander("🤝 Partner Network", expanded=True):
        st.metric("High Reliability Partners", st.session_state.metric_partners)

# COLUMN 2: AI BRAIN
with col2:
    st.subheader("🧠 Executive Briefing")
    
    if st.button("⚡ Run AI Analysis", use_container_width=True):
        with st.spinner("OmniSight is synthesizing data..."):
            analysis_text = ai_engine.analyze_state(st.session_state.state_data)
            st.session_state.briefing = analysis_text
            
    st.info(st.session_state.briefing)
    
    st.markdown("##### 📈 Strategic Impact Trend")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Revenue Risk', 'Ops Strain', 'Market Volatility'])
    st.area_chart(chart_data, color=["#6f42c1", "#2e1a47", "#dcd3e9"])

# COLUMN 3: STRATEGY CHAT
with col3:
    st.subheader("💬 Strategy Chat")
    user_input = st.text_input("Consult OmniSight:", placeholder="Ask about the ripple...")
    if user_input:
        with st.spinner("Thinking..."):
            response = ai_engine.ask_ai_question(user_input, st.session_state.state_data)
            st.markdown(f"**OmniSight AI:**\n\n{response}")

# --- 5. SIDEBAR: SIMULATION TOOLS ---
with st.sidebar:
    st.header("🎮 Simulation Center")
    if st.button("🔄 Refresh Data Feed"):
        data, rev, ops, partners = refresh_data()
        st.session_state.state_data = data
        st.session_state.metric_revenue = rev
        st.session_state.metric_ops = ops
        st.session_state.metric_partners = partners
        st.rerun()
    
    st.divider()
    if st.button("🔄 Reset Dashboard"):
        st.session_state.clear()
        st.rerun()