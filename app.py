import streamlit as st
import time
<<<<<<< HEAD
import ai_engine       # Your Brain
import data_generator  # Your Data Source
=======
from openai import OpenAI

# --- CUSTOM MODULES ---
import ai_engine       # The Brain
import data_generator  # The Data Source
>>>>>>> 662328e2dbd9c0b656a6f91f9f553732f2ab402d

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="OmniSight AI | Enterprise Nervous System",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

<<<<<<< HEAD
# Custom Styling to make it look like a pro dashboard
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #00f2ea; }
    .stButton>button { background-color: #00f2ea; color: #000000; border-radius: 8px; font-weight: bold;}
    .reportview-container .main .block-container { max-width: 1200px; }
    h1 { color: #00f2ea; }
    h2, h3 { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING & STATE MANAGEMENT ---
def load_data():
    """Fetches fresh data from the generator."""
    return {
        "finance": data_generator.get_financial_data(),
        "operations": data_generator.get_operations_data(),
        "partners": data_generator.get_partner_data(),
        "clients": data_generator.get_client_data()
    }
=======
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
>>>>>>> 662328e2dbd9c0b656a6f91f9f553732f2ab402d

# Initialize Session State (so data stays consistent until you refresh)
if 'state_data' not in st.session_state:
<<<<<<< HEAD
    st.session_state.state_data = load_data()
    st.session_state.ai_analysis = None # Store analysis so it doesn't disappear

# --- 3. METRIC CALCULATIONS ---
current_data = st.session_state.state_data

# Calculate Revenue (Sum of all 'Income')
total_revenue = sum(item['amount'] for item in current_data['finance'] if item['type'] == 'Income')
# Calculate Active Operations
active_ops = sum(1 for item in current_data['operations'] if item['status'] == 'Active')
# Calculate Partner Reliability Count
reliable_partners = sum(1 for item in current_data['partners'] if item['reliability'] == 'High')

# --- 4. SIDEBAR (SIMULATION) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/825/825590.png", width=80)
    st.title("OmniSight Control")
    st.markdown("---")
    
    st.markdown("### 🎮 Simulation Lab")
    if st.button("🔄 Refresh Data Feed", use_container_width=True):
        with st.spinner("Simulating new data stream..."):
            time.sleep(1) # Fake loading for effect
            st.session_state.state_data = load_data()
            st.session_state.ai_analysis = None # Reset analysis on new data
            st.rerun()
            
    st.info(f"System Status: **ONLINE**\n\nConnected to: **Gemini 1.5 Flash**")

# --- 5. MAIN DASHBOARD UI ---

# Header
st.title("👁️ OmniSight AI")
st.markdown("#### The Enterprise Nervous System: Unifying Finance, Ops, and Partners.")
st.divider()

# ROW 1: THE "GOD VIEW" (Scoreboard)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"${total_revenue:,.0f}", delta="+12%")
with col2:
    st.metric("⚙️ Active Production", f"{active_ops} Lines", delta="Stable")
with col3:
    st.metric("🤝 Reliable Partners", f"{reliable_partners} / {len(current_data['partners'])}", delta="-1")
with col4:
    st.metric("👥 Active Clients", f"{len(current_data['clients'])}", delta="No Change")

# ROW 2: THE "WHY ENGINE" (AI Analysis)
st.divider()
st.subheader("🧠 Executive Intelligence Briefing")

# The "Magic Button"
if st.button("⚡ Analyze Cross-Domain Risks", use_container_width=True):
    with st.spinner("OmniSight is connecting the dots across 4 domains..."):
        # CALL YOUR BRAIN
        analysis_text = ai_engine.analyze_state(current_data)
        st.session_state.ai_analysis = analysis_text

# Display the Analysis if it exists
if st.session_state.ai_analysis:
    st.success("Analysis Complete")
    st.markdown(f"""
    <div style="background-color: #1e2130; padding: 20px; border-radius: 10px; border-left: 5px solid #00f2ea;">
        {st.session_state.ai_analysis}
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("System Standby. Click 'Analyze' to detect hidden risks.")

# ROW 3: THE "SMART CONSULTANT" (Chat)
st.divider()
col_chat_input, col_chat_output = st.columns([1, 2])

with col_chat_input:
    st.subheader("💬 Ask the Data")
    user_q = st.text_input("Query the system:", placeholder="e.g. Which partner is causing the risk?")
    
    if user_q:
        with st.spinner("Thinking..."):
            # CALL YOUR BRAIN (Chat function)
            answer = ai_engine.ask_ai_question(user_q, current_data)
            
            # Show result in the right column
            with col_chat_output:
                st.subheader("💡 OmniSight Answer")
                st.write(answer)
=======
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
>>>>>>> 662328e2dbd9c0b656a6f91f9f553732f2ab402d
