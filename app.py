import streamlit as st
import textwrap
import re

import ai_engine
import data_generator

from views import dashboard, deepdive, predictive, scenario

def icon_eye(size=18, color="currentColor"):
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"
viewBox="0 0 24 24" fill="none" stroke="{color}"
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
  <circle cx="12" cy="12" r="3"/>
</svg>
"""

st.set_page_config(
    page_title="OmniSight AI",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
  background:
    radial-gradient(1200px 700px at 20% 0%, rgba(34,211,238,0.10), transparent 60%),
    radial-gradient(900px 600px at 90% 10%, rgba(99,102,241,0.10), transparent 55%),
    #0b0f17;
  color: #e5e7eb;
}

.block-container {
  padding-top: 1.4rem;
  padding-bottom: 2rem;
  max-width: 1200px;
}

.small-muted {
  color: rgba(229,231,235,0.65);
  font-size: 0.92rem;
}

/* Top bar */
.os-topbar {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding: 14px 18px;
  border-radius: 18px;
  background: rgba(17,24,39,0.72);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}

.os-title {
  font-weight: 850;
  font-size: 1.05rem;
  letter-spacing: -0.02em;
}

.os-sub {
  color: rgba(229,231,235,0.60);
  font-size: 0.88rem;
  margin-top: 2px;
}

/* Cards / Boxes */
.os-card{
  background: rgba(17,24,39,0.70);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

/* Briefing box */
.os-brief{
  background: rgba(17,24,39,0.55);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 16px;
  line-height: 1.45;
}

/* KPI card internals (used in dashboard.py) */
.os-kpi-top{ display:flex; justify-content:space-between; align-items:center; }
.os-kpi-label{ font-size: 0.85rem; color: rgba(229,231,235,0.70); }
.os-kpi-value{ font-size: 1.35rem; font-weight: 850; margin-top: 6px; }
.os-kpi-delta{ font-size: 0.80rem; font-weight: 650; }
.delta-pos{ color: rgba(34,211,238,0.95); }
.delta-neg{ color: rgba(255,181,114,0.95); }
.delta-neutral{ color: rgba(229,231,235,0.55); }

/* Tabs (centered, white active) */
.stTabs [data-baseweb="tab-list"] {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 32px !important;
  margin-top: 18px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.stTabs [data-baseweb="tab"] {
  color: rgba(229,231,235,0.70) !important;
  font-weight: 500;
  background: transparent !important;
  border: none !important;
  padding: 10px 6px;
}

.stTabs [data-baseweb="tab"]:hover {
  color: #e5e7eb !important;
}

.stTabs [aria-selected="true"] {
  color: #ffffff !important;
  font-weight: 700 !important;
}

.stTabs [aria-selected="true"]::after {
  content: "";
  display: block;
  height: 3px;
  width: 100%;
  margin-top: 6px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    rgba(34,211,238,1),
    rgba(99,102,241,1)
  );
}

/* Buttons */
div.stButton > button {
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.06);
  color: #e5e7eb;
  padding: 0.7rem 1rem;
}

div.stButton > button:hover {
  border-color: rgba(34,211,238,0.60);
  background: rgba(34,211,238,0.10);
}
</style>
""",
    unsafe_allow_html=True,
)

def ss_default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


ss_default("current_data", data_generator.generate_full_dataset())
ss_default("ai_analysis", "")
ss_default("prediction", "")
ss_default("scenario_result", "")
ss_default("deepdive_result", "")

topbar_html = f"""
<div class="os-topbar">
  <div style="display:flex; gap:12px; align-items:center;">
    {icon_eye(18)}
    <div>
      <div class="os-title">OmniSight AI</div>
      <div class="os-sub">See the ripple • Real-time Enterprise Intelligence</div>
    </div>
  </div>
  <div class="small-muted">Demo Mode</div>
</div>
"""

safe_topbar = textwrap.dedent(topbar_html).strip()
safe_topbar = re.sub(r"(?m)^[ \t]{4,}", "", safe_topbar)
st.markdown(safe_topbar, unsafe_allow_html=True)

tabs = st.tabs(["Executive Overview", "Business Signals", "Risk & Forecast", "What-If Scenarios"])

with tabs[0]:
    dashboard.show(st.session_state.current_data, ai_engine)

with tabs[1]:
    deepdive.show(st.session_state.current_data, ai_engine)

with tabs[2]:
    predictive.show(st.session_state.current_data, ai_engine)

with tabs[3]:
    scenario.show(st.session_state.current_data, ai_engine)
