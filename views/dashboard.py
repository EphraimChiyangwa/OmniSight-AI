import streamlit as st
from pathlib import Path

import data_generator


def _logo_path():
    root = Path(__file__).resolve().parent.parent
    p = root / "image" / "OmniSightLogo.png"
    return str(p) if p.exists() else None


def show(current_data, ai_engine):
    # ---- ensure state keys exist ----
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = ""

    # ---- load domains ----
    finance = current_data.get("finance", [])
    ops = current_data.get("operations", [])
    partners = current_data.get("partners", [])
    clients = current_data.get("clients", [])
    compliance = current_data.get("compliance", [])

    # ---- KPIs ----
    total_rev_7d = sum(
        t.get("amount", 0) for t in finance
        if t.get("type") == "Income"
    )

    active_lines = sum(1 for o in ops if o.get("status") in ("Active", "Degraded"))
    reliable_partners = sum(1 for p in partners if p.get("relationship_health", 0) >= 0.75)
    active_clients = sum(1 for c in clients if c.get("status") == "Active")

    avg_compliance = (sum(x.get("compliance_score", 0) for x in compliance) / len(compliance)) if compliance else 1.0
    avg_churn = (sum(c.get("churn_risk", 0) for c in clients) / len(clients)) if clients else 0.0
    risk_score = round(((1 - avg_compliance) * 60 + (avg_churn * 40)) * 100, 2)

    # ---- optional smaller logo (minimal) ----
    logo = _logo_path()
    if logo:
        c1, c2, c3 = st.columns([1.2, 1, 1.2])
        with c2:
            st.image(logo, width=320)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---- KPI row ----
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, label, value, delta_text, delta_class):
        with col:
            st.markdown(
                f"""
<div class="os-card">
  <div class="os-kpi-top">
    <div class="os-kpi-label">{label}</div>
    <div class="os-kpi-delta {delta_class}">{delta_text}</div>
  </div>
  <div class="os-kpi-value">{value}</div>
</div>
""",
                unsafe_allow_html=True
            )

    kpi(k1, "Revenue (Demo)", f"${total_rev_7d:,.0f}", "+ trend", "delta-pos")
    kpi(k2, "Production", f"{active_lines} lines", "stable", "delta-neutral")
    kpi(k3, "Partners", f"{reliable_partners}/{max(len(partners),1)}", "watch", "delta-neg")
    kpi(k4, "Clients", f"{active_clients}", "ok", "delta-neutral")
    kpi(k5, "Risk Score", f"{risk_score:.2f}", "priority", "delta-neg" if risk_score > 35 else "delta-pos")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ---- Actions row ----
    a1, a2, a3 = st.columns([1, 2, 1])
    with a2:
        if st.button("Refresh Data Feed", use_container_width=True):
            st.session_state.current_data = data_generator.generate_full_dataset()
            st.session_state.ai_analysis = ""
            st.rerun()

        if st.button("Analyze Cross-Domain Risks", use_container_width=True):
            with st.spinner("Synthesizing intelligence..."):
                # IMPORTANT: keep your existing AI engine behavior
                st.session_state.ai_analysis = ai_engine.analyze_state(st.session_state.current_data)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ---- Hybrid layout: AI Briefing + Status ----
    left, right = st.columns([3, 1])

    with left:
        if st.session_state.ai_analysis:
            st.markdown(f"<div class='os-brief'>{st.session_state.ai_analysis}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='os-brief'><span class='small-muted'>System ready.</span> Click <b>Analyze</b> to surface hidden cross-domain causes and impacts.</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='small-muted'>Ask the Data</div>", unsafe_allow_html=True)
        
        q = st.text_input("", placeholder="e.g. What triggered the churn risk in APAC?", label_visibility="collapsed")
        if q:
            with st.spinner("Reasoning..."):
                ans = ai_engine.ask_ai_question(q, st.session_state.current_data)
            st.markdown(f"<div class='os-card'><b>Insight:</b> {ans}</div>", unsafe_allow_html=True)

    with right:
        generated_at = current_data.get("generated_at", "—")
        st.markdown(
            f"""
<div class="os-card">
  <div style="font-weight:850; font-size:0.95rem;">System</div>
  <div style="margin-top:10px" class="small-muted">Status: <b>ONLINE</b></div>
  <div class="small-muted">Updated: <b>{generated_at}</b></div>
  <div style="height:10px"></div>
  <div class="small-muted">Model: <b>Gemini 1.5 Flash</b></div>
</div>
""",
            unsafe_allow_html=True
        )
