"""
Enhanced OmniSight-AI Application
Now with 6 domains, predictive analytics, scenario modeling, and more!
"""

import streamlit as st
import time
import ai_engine as ai_engine  # CHANGED: Fixed import to match standard filename
import data_generator as data_generator  # CHANGED: Fixed import to match standard filename
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="OmniSight AI | Enterprise Intelligence System",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #00f2ea; }
    div[data-testid="stMetricDelta"] { font-size: 14px; }
    .stButton>button { 
        background-color: #00f2ea; 
        color: #000000; 
        border-radius: 8px; 
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00d4cc;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 242, 234, 0.4);
    }
    .reportview-container .main .block-container { max-width: 1400px; }
    h1 { color: #00f2ea; text-align: center; }
    h2, h3 { color: #ffffff; }
    .success-box { 
        background-color: #1e2130; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #00f2ea;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #2d1e1e;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff6b6b;
        margin: 10px 0;
    }
    .info-box {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4ecdc4;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING & STATE MANAGEMENT ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """Fetches fresh data from the enhanced generator."""
    return {
        "finance": data_generator.get_financial_data(),
        "operations": data_generator.get_operations_data(),
        "partners": data_generator.get_partner_data(),
        "clients": data_generator.get_client_data(),
        "competitive": data_generator.get_competitive_data(),
        "compliance": data_generator.get_compliance_data()
    }

# Initialize Session State
if 'state_data' not in st.session_state:
    st.session_state.state_data = load_data()
    st.session_state.ai_analysis = None
    st.session_state.prediction = None
    st.session_state.scenario_result = None
    st.session_state.chat_history = []

# --- 3. ENHANCED METRIC CALCULATIONS ---
current_data = st.session_state.state_data
metrics = data_generator.get_aggregated_metrics()

# Calculate key metrics
total_revenue = sum(item['amount'] for item in current_data['finance'][:7] if item['type'] == 'Income')
previous_revenue = sum(item['amount'] for item in current_data['finance'][7:14] if item['type'] == 'Income')
revenue_change_pct = ((total_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0

active_ops = sum(1 for item in current_data['operations'] if item['status'] in ['Active', 'Degraded'])
degraded_ops = sum(1 for item in current_data['operations'] if item['status'] == 'Degraded')

reliable_partners = sum(1 for item in current_data['partners'] if item['reliability'] == 'High')
at_risk_partners = sum(1 for item in current_data['partners'] if item.get('relationship_health', 1.0) < 0.75)

high_risk_clients = sum(1 for item in current_data['clients'] if item.get('churn_risk', 0) > 0.25)

# --- 4. SIDEBAR (ENHANCED CONTROLS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/825/825590.png", width=80)
    st.title("OmniSight Control")
    st.markdown("---")
    
    # System Status
    st.markdown("### 🎮 System Status")
    st.success("**ONLINE** - All Systems Operational")
    st.info(f"AI Model: **Gemini 1.5 Flash**\n\nData Domains: **6/6 Active**")
    
    st.markdown("---")
    
    # Data Controls
    st.markdown("### 📊 Data Controls")
    if st.button("🔄 Refresh Data Feed", use_container_width=True):
        with st.spinner("Refreshing enterprise data..."):
            time.sleep(1)
            st.cache_data.clear()
            st.session_state.state_data = load_data()
            st.session_state.ai_analysis = None
            st.session_state.prediction = None
            st.rerun()
    
    # View selector
    st.markdown("---")
    st.markdown("### 👁️ View Mode")
    view_mode = st.radio(
        "Select View:",
        ["Executive Dashboard", "Domain Deep Dive", "Predictive Analytics", "Scenario Modeling"],
        label_visibility="collapsed"
    )
    
    # Domain selector for deep dive
    if view_mode == "Domain Deep Dive":
        selected_domain = st.selectbox(
            "Select Domain:",
            ["Financial", "Operations", "Partners", "Clients", "Competitive", "Compliance"]
        )
    
    st.markdown("---")
    st.markdown("### 📅 Last Updated")
    st.text(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- 5. MAIN DASHBOARD UI ---

# Header with dynamic status
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("👁️ OmniSight AI")
    st.markdown("#### Real-Time Enterprise Intelligence Across All Domains")
with col_status:
    # Dynamic status indicator
    if at_risk_partners > 0 or high_risk_clients > 2 or degraded_ops > 0:
        st.error("⚠️ ALERTS ACTIVE")
    else:
        st.success("✅ ALL CLEAR")

st.divider()

# --- EXECUTIVE DASHBOARD VIEW ---
if view_mode == "Executive Dashboard":
    
    # ROW 1: KEY METRICS (Enhanced with 6 domains)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        delta_color = "normal" if revenue_change_pct >= 0 else "inverse"
        st.metric(
            "💰 Revenue (7d)", 
            f"${total_revenue:,.0f}", 
            delta=f"{revenue_change_pct:+.1f}%",
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            "⚙️ Operations", 
            f"{active_ops} Active",
            delta=f"{degraded_ops} Degraded" if degraded_ops > 0 else "Stable",
            delta_color="inverse" if degraded_ops > 0 else "off"
        )
    
    with col3:
        st.metric(
            "🤝 Partners", 
            f"{reliable_partners}/{len(current_data['partners'])}",
            delta=f"{at_risk_partners} At Risk" if at_risk_partners > 0 else "Healthy",
            delta_color="inverse" if at_risk_partners > 0 else "normal"
        )
    
    with col4:
        st.metric(
            "👥 Clients", 
            f"{len(current_data['clients'])}",
            delta=f"{high_risk_clients} High Risk" if high_risk_clients > 0 else "Stable",
            delta_color="inverse" if high_risk_clients > 0 else "off"
        )
    
    with col5:
        competitive_threats = len([c for c in current_data['competitive'] if c.get('threat_level') == 'High'])
        st.metric(
            "🎯 Competition", 
            f"{len(current_data['competitive'])} Tracked",
            delta=f"{competitive_threats} High Threat" if competitive_threats > 0 else "Monitored",
            delta_color="inverse" if competitive_threats > 0 else "off"
        )
    
    with col6:
        compliance_issues = sum(c.get('issues', 0) for c in current_data['compliance'])
        st.metric(
            "⚖️ Compliance", 
            f"{len(current_data['compliance'])} Domains",
            delta=f"{compliance_issues} Issues" if compliance_issues > 0 else "Compliant",
            delta_color="inverse" if compliance_issues > 0 else "normal"
        )
    
    st.divider()
    
    # ROW 2: AI ANALYSIS (Enhanced)
    st.subheader("🧠 Cross-Domain Intelligence Analysis")
    
    col_analyze, col_predict = st.columns(2)
    
    with col_analyze:
        if st.button("⚡ Analyze Current State", use_container_width=True, type="primary"):
            with st.spinner("🔍 OmniSight is performing cross-domain analysis..."):
                analysis_text = ai_engine.analyze_state(current_data)
                st.session_state.ai_analysis = analysis_text
    
    with col_predict:
        if st.button("🔮 Generate Predictive Forecast", use_container_width=True):
            with st.spinner("📊 Running predictive models..."):
                prediction = ai_engine.predict_future_state(current_data, "30 days")
                st.session_state.prediction = prediction
    
    # Display Analysis
    if st.session_state.ai_analysis:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.ai_analysis)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Click 'Analyze Current State' to receive cross-domain intelligence insights")
    
    # Display Prediction
    if st.session_state.prediction:
        st.divider()
        st.subheader("🔮 30-Day Forecast")
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.prediction)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # ROW 3: INTERACTIVE Q&A
    st.subheader("💬 Ask OmniSight Anything")
    
    col_input, col_clear = st.columns([5, 1])
    
    with col_input:
        user_q = st.text_input(
            "Query the system:",
            placeholder="e.g. Why is revenue declining? Which partner is causing the most risk?",
            label_visibility="collapsed"
        )
    
    with col_clear:
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    if user_q:
        with st.spinner("🤔 Processing your query..."):
            answer = ai_engine.ask_ai_question(user_q, current_data)
            st.session_state.chat_history.append({"q": user_q, "a": answer})
    
    # Display chat history
    if st.session_state.chat_history:
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
            with st.container():
                st.markdown(f"**❓ Question:** {chat['q']}")
                st.markdown(f"**💡 Answer:** {chat['a']}")
                st.markdown("---")

# --- DOMAIN DEEP DIVE VIEW ---
elif view_mode == "Domain Deep Dive":
    st.subheader(f"🔍 {selected_domain} Domain Analysis")
    
    # Get domain-specific data
    domain_key = selected_domain.lower()
    if domain_key in current_data:
        domain_data = current_data[domain_key]
        
        # Display raw data
        st.markdown("### 📊 Current Data")
        st.json(domain_data)
        
        # AI Analysis of specific domain
        if st.button(f"🧠 Analyze {selected_domain} Domain", use_container_width=True, type="primary"):
            with st.spinner(f"Analyzing {selected_domain}..."):
                analysis = ai_engine.analyze_specific_domain(selected_domain, domain_data)
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(analysis)
                st.markdown('</div>', unsafe_allow_html=True)

# --- PREDICTIVE ANALYTICS VIEW ---
elif view_mode == "Predictive Analytics":
    st.subheader("🔮 Predictive Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        forecast_period = st.selectbox("Forecast Period:", ["7 days", "30 days", "90 days", "1 year"])
    
    with col2:
        if st.button("🚀 Generate Forecast", use_container_width=True, type="primary"):
            with st.spinner(f"Generating {forecast_period} forecast..."):
                prediction = ai_engine.predict_future_state(current_data, forecast_period)
                st.session_state.prediction = prediction
    
    if st.session_state.prediction:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.prediction)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select a forecast period and click 'Generate Forecast'")
    
    # Morning Briefing
    st.divider()
    st.subheader("🌅 Automated Executive Briefing")
    if st.button("📋 Generate Daily Briefing", use_container_width=True):
        with st.spinner("Creating your executive briefing..."):
            briefing = ai_engine.generate_executive_briefing(current_data)
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(briefing)
            st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO MODELING VIEW ---
elif view_mode == "Scenario Modeling":
    st.subheader("🎭 What-If Scenario Modeling")
    
    st.markdown("Model the impact of potential business scenarios across all domains.")
    
    # Pre-defined scenarios
    st.markdown("### 📋 Common Scenarios")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Increase Marketing Budget by 50%", use_container_width=True):
            scenario = "Increase marketing budget by 50%"
            with st.spinner("Modeling scenario impact..."):
                result = ai_engine.simulate_scenario(scenario, current_data)
                st.session_state.scenario_result = result
    
    with col2:
        if st.button("🤝 Lose Top Partner", use_container_width=True):
            scenario = "Our top partner (XYZ Logistics) terminates the relationship"
            with st.spinner("Modeling scenario impact..."):
                result = ai_engine.simulate_scenario(scenario, current_data)
                st.session_state.scenario_result = result
    
    with col3:
        if st.button("🎯 Competitor Acquisition", use_container_width=True):
            scenario = "Competitor A acquires Competitor B"
            with st.spinner("Modeling scenario impact..."):
                result = ai_engine.simulate_scenario(scenario, current_data)
                st.session_state.scenario_result = result
    
    st.divider()
    
    # Custom scenario
    st.markdown("### ✏️ Custom Scenario")
    custom_scenario = st.text_area(
        "Describe your scenario:",
        placeholder="e.g. We raise prices by 15% in APAC region",
        height=100
    )
    
    if st.button("🔬 Model Custom Scenario", use_container_width=True, type="primary"):
        if custom_scenario:
            with st.spinner("Analyzing scenario impact..."):
                result = ai_engine.simulate_scenario(custom_scenario, current_data)
                st.session_state.scenario_result = result
        else:
            st.warning("Please describe a scenario first")
    
    # Display results
    if st.session_state.scenario_result:
        st.divider()
        st.markdown("### 📊 Scenario Analysis Results")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.scenario_result)
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🚀 OmniSight AI - Enterprise Intelligence Platform")
with col2:
    st.caption("🧠 Powered by Gemini 1.5 Flash")
with col3:
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")