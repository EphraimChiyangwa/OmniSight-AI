from pathlib import Path
import streamlit as st

import ai_engine
import data_generator

from views import dashboard, deepdive, predictive, scenario


# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="OmniSight AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Design system (minimal dark)
# ----------------------------
st.markdown(
    """
<style>
/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Base */
.stApp {
  background: radial-gradient(1200px 700px at 20% 0%, rgba(34,211,238,0.10), transparent 60%),
              radial-gradient(900px 600px at 90% 10%, rgba(99,102,241,0.10), transparent 55%),
              #0b0f17;
  color: #e5e7eb;
}
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px; }

/* Typography */
h1, h2, h3 { letter-spacing: -0.02em; }
.small-muted { color: rgba(229,231,235,0.65); font-size: 0.92rem; }

/* Top bar */
.os-topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(17,24,39,0.72);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  backdrop-filter: blur(8px);
}
.os-brand{ display:flex; gap:10px; align-items:center; }
.os-dot{
  width:10px; height:10px; border-radius:999px;
  background: rgba(34,211,238,0.95);
  box-shadow: 0 0 18px rgba(34,211,238,0.55);
}
.os-title{ font-weight: 800; font-size: 1.05rem; }
.os-sub{ color: rgba(229,231,235,0.60); font-size: 0.88rem; margin-top: 1px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 22px; justify-content: center; margin-top: 14px; }
.stTabs [data-baseweb="tab"] {
  padding: 10px 6px;
  background: transparent !important;
  border-radius: 12px;
  color: rgba(229,231,235,0.75);
}
.stTabs [aria-selected="true"] {
  color: #e5e7eb !important;
  border-bottom: 2px solid rgba(34,211,238,0.95);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 14px; }

/* Cards */
.os-card{
  background: rgba(17,24,39,0.70);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

/* KPI cards */
.os-kpi-top{ display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px; }
.os-kpi-label{ font-size: 0.78rem; color: rgba(229,231,235,0.60); letter-spacing: .10em; text-transform: uppercase; }
.os-kpi-value{ font-size: 1.55rem; font-weight: 850; letter-spacing: -0.02em; }
.os-kpi-delta{ font-size: 0.85rem; font-weight: 700; }
.delta-pos{ color: rgba(72,187,120,0.95); }
.delta-neg{ color: rgba(245,101,101,0.95); }
.delta-neutral{ color: rgba(229,231,235,0.75); }

/* AI briefing */
.os-brief{
  background: rgba(15,23,42,0.65);
  border: 1px solid rgba(255,255,255,0.08);
  border-left: 4px solid rgba(34,211,238,0.95);
  border-radius: 16px;
  padding: 16px;
  line-height: 1.55;
}

/* Buttons */
div.stButton > button {
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.06);
  color: #e5e7eb;
  padding: 0.70rem 1rem;
}
div.stButton > button:hover {
  border-color: rgba(34,211,238,0.60);
  background: rgba(34,211,238,0.10);
}

/* Inputs */
.stTextInput input {
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #e5e7eb !important;
}
</style>
"""

,
    unsafe_allow_html=True,
)

# ----------------------------
# Session state (prevent crashes)
# ----------------------------
def ss_default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

ss_default("current_data", data_generator.generate_full_dataset())
ss_default("ai_analysis", "")
ss_default("prediction", "")
ss_default("scenario_result", "")
ss_default("deepdive_result", "")

# ----------------------------
# Top bar
# ----------------------------
st.markdown(
    """
<div class="os-topbar">
  <div class="os-brand">
    <div class="os-dot"></div>
    <div>
      <div class="os-title">OmniSight AI</div>
      <div class="os-sub">See the ripple • Real-time Enterprise Intelligence</div>
    </div>
  </div>
  <div class="small-muted">Demo Mode</div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Navigation (Hybrid)
# ----------------------------
tabs = st.tabs(["Dashboard", "Deep Dive", "Prediction", "Scenarios"])

with tabs[0]:
    dashboard.show(st.session_state.current_data, ai_engine)

with tabs[1]:
    deepdive.show(st.session_state.current_data, ai_engine)

with tabs[2]:
    predictive.show(st.session_state.current_data, ai_engine)

with tabs[3]:
    scenario.show(st.session_state.current_data, ai_engine)
