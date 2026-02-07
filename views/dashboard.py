from pathlib import Path
from datetime import datetime
import random
import time

import streamlit as st

import data_generator


# =================================================
# CONFIG
# =================================================
REFRESH_SECONDS = 5
MAX_POINTS = 60  # chart history points


def _logo_path():
    root = Path(__file__).resolve().parent.parent
    p = root / "image" / "OmniSightLogo.png"
    return str(p) if p.exists() else None


# =================================================
# CSS (Chart card matches your noir gradient aesthetic)
# =================================================
def _inject_chart_css():
    st.markdown(
        """
<style>
.os-chart-card{
  width: 100%;
  height: 400px;
  border-radius: 16px;
  background: linear-gradient(133.84deg, #4E4E4E -16.04%, #333333 9.33%, #1A1A1A 32.02%, #1A1A1A 62.06%, #262626 87.42%, #4E4E4E 112.12%);
  box-shadow: 2px 6px 15px 2px rgba(12, 10, 11, 0.8);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}

.os-chart-head{
  height: 72px;
  padding: 10px 16px;
  display:flex;
  align-items:center;
  justify-content:space-between;
}

.os-chart-divider{
  height: 1px;
  width: 100%;
  background: rgba(255,255,255,0.85);
}

.os-chart-title{
  display:flex;
  flex-direction:column;
  gap:2px;
}

.os-chart-title .h6{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  font-weight: 600;
  font-size: 20px;
  line-height: 28px;
  letter-spacing: 0.15px;
  color:#FFFFFF;
}

.os-chart-title .sub{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.005em;
  color:#D9D9D9;
}

.os-chart-body{
  height: calc(400px - 72px - 1px);
  padding: 12px 12px 12px 12px;
}

/* Make plot backgrounds transparent so the gradient card shows */
.os-chart-body iframe, .os-chart-body svg, .os-chart-body canvas {
  background: transparent !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


# =================================================
# REAL-TIME STATE
# =================================================
def _init_live_state():
    if "live_on" not in st.session_state:
        st.session_state.live_on = True
    if "series" not in st.session_state:
        st.session_state.series = {"t": [], "revenue": [], "risk": []}
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = ""


def _calc_kpis(current_data):
    finance = current_data.get("finance", [])
    ops = current_data.get("operations", [])
    partners = current_data.get("partners", [])
    clients = current_data.get("clients", [])
    compliance = current_data.get("compliance", [])

    total_rev_7d = sum(t.get("amount", 0) for t in finance if t.get("type") == "Income")

    active_lines = sum(1 for o in ops if o.get("status") in ("Active", "Degraded"))
    reliable_partners = sum(1 for p in partners if p.get("relationship_health", 0) >= 0.75)
    active_clients = sum(1 for c in clients if c.get("status") == "Active")

    avg_compliance = (sum(x.get("compliance_score", 0) for x in compliance) / len(compliance)) if compliance else 1.0
    avg_churn = (sum(c.get("churn_risk", 0) for c in clients) / len(clients)) if clients else 0.0
    risk_score = round(((1 - avg_compliance) * 60 + (avg_churn * 40)) * 100, 2)

    return {
        "total_rev_7d": float(total_rev_7d),
        "active_lines": int(active_lines),
        "reliable_partners": int(reliable_partners),
        "partners_total": int(max(len(partners), 1)),
        "active_clients": int(active_clients),
        "risk_score": float(risk_score),
    }


def _apply_drift(current_data):
    """
    Realistic micro-movements:
    - Revenue drifts slightly up/down
    - Churn risk shifts slightly
    - Compliance shifts slightly
    This makes risk_score and revenue move naturally.
    """
    finance = current_data.get("finance", [])
    clients = current_data.get("clients", [])
    compliance = current_data.get("compliance", [])

    # Revenue drift (±1.5%)
    rev_mult = 1.0 + random.uniform(-0.015, 0.015)
    for t in finance[:30]:
        if isinstance(t, dict) and t.get("type") == "Income":
            amt = t.get("amount", 0)
            if isinstance(amt, (int, float)):
                t["amount"] = max(0.0, amt * rev_mult)

    # Churn drift (0..1)
    churn_shift = random.uniform(-0.01, 0.02)
    for c in clients[:100]:
        if isinstance(c, dict):
            r = c.get("churn_risk", 0.0)
            if isinstance(r, (int, float)):
                c["churn_risk"] = min(max(r + churn_shift, 0.0), 1.0)

    # Compliance drift (0..1)
    comp_shift = random.uniform(-0.01, 0.01)
    for x in compliance[:80]:
        if isinstance(x, dict):
            cs = x.get("compliance_score", 1.0)
            if isinstance(cs, (int, float)):
                x["compliance_score"] = min(max(cs + comp_shift, 0.0), 1.0)

    current_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_data


# =================================================
# CHART (Plotly if available; else Streamlit line_chart fallback)
# =================================================
def _try_plotly():
    try:
        import plotly.graph_objects as go
        return go
    except Exception:
        return None


def _render_chart_card(title, subtitle, fig_or_df, use_plotly: bool):
    st.markdown(
        f"""
<div class="os-chart-card">
  <div class="os-chart-head">
    <div class="os-chart-title">
      <div class="h6">{title}</div>
      <div class="sub">{subtitle}</div>
    </div>
  </div>
  <div class="os-chart-divider"></div>
  <div class="os-chart-body">
        """,
        unsafe_allow_html=True,
    )

    if use_plotly:
        st.plotly_chart(fig_or_df, use_container_width=True, config={"displayModeBar": False})
    else:
        # fallback chart (less pretty, but works)
        st.line_chart(fig_or_df, use_container_width=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


def _build_plotly_line(go, x, y, name):
    # Noir dashboard style + purple accent (#9290FE)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=3, color="#9290FE"),
            name=name,
        )
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#D9D9D9"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(77,77,77,0.45)",
            zeroline=False,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(77,77,77,0.45)",
            zeroline=False,
            tickfont=dict(size=10),
        ),
        showlegend=False,
    )
    return fig


# =================================================
# MAIN VIEW
# =================================================
def show(current_data, ai_engine):
    _inject_chart_css()
    _init_live_state()

    # Ensure dataset persists across reruns
    if "current_data" not in st.session_state or not isinstance(st.session_state.current_data, dict):
        st.session_state.current_data = current_data

    # Logo
    logo = _logo_path()
    if logo:
        c1, c2, c3 = st.columns([1.2, 1, 1.2])
        with c2:
            st.image(logo, width=320)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Controls row (keep main feature)
    ctrl1, ctrl2, ctrl3 = st.columns([1, 2, 1])
    with ctrl1:
        st.session_state.live_on = st.toggle("Live Mode", value=st.session_state.live_on)
    with ctrl2:
        st.caption(f"Real-time simulation updates every {REFRESH_SECONDS}s")
    with ctrl3:
        if st.button("Reset Dataset", use_container_width=True):
            st.session_state.current_data = data_generator.generate_full_dataset()
            st.session_state.series = {"t": [], "revenue": [], "risk": []}
            st.session_state.ai_analysis = ""
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---------- PARTIAL REFRESH SECTION ----------
    # This is the key change:
    # Use Streamlit fragments to update ONLY KPIs + Charts every 5s
    fragment = getattr(st, "fragment", None)

    def _render_kpi_row(kpis):
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

        # Deltas from series
        rev_delta = "stable"
        risk_delta = "stable"
        s = st.session_state.series
        if len(s["revenue"]) >= 2:
            rev_delta = "up" if s["revenue"][-1] >= s["revenue"][-2] else "down"
        if len(s["risk"]) >= 2:
            risk_delta = "up" if s["risk"][-1] >= s["risk"][-2] else "down"

        kpi(k1, "Revenue (7d)", f"${kpis['total_rev_7d']:,.0f}", rev_delta,
            "delta-pos" if rev_delta == "up" else ("delta-neg" if rev_delta == "down" else "delta-neutral"))
        kpi(k2, "Production", f"{kpis['active_lines']} lines", "stable", "delta-neutral")
        kpi(k3, "Partners", f"{kpis['reliable_partners']}/{kpis['partners_total']}", "watch", "delta-neg")
        kpi(k4, "Clients", f"{kpis['active_clients']}", "ok", "delta-neutral")
        kpi(k5, "Risk Score", f"{kpis['risk_score']:.2f}", risk_delta,
            "delta-neg" if risk_delta == "up" else ("delta-pos" if risk_delta == "down" else "delta-neutral"))

    def _render_charts():
        # Prepare series
        t = st.session_state.series["t"]
        rev = st.session_state.series["revenue"]
        risk = st.session_state.series["risk"]

        go = _try_plotly()
        use_plotly = go is not None

        cL, cR = st.columns(2)
        with cL:
            if use_plotly and len(t) >= 2:
                fig = _build_plotly_line(go, t, rev, "Revenue")
                _render_chart_card("Last updates", "Revenue (rolling)", fig, True)
            else:
                # fallback
                import pandas as pd
                df = pd.DataFrame({"Revenue": rev}, index=t) if t else pd.DataFrame({"Revenue": []})
                _render_chart_card("Last updates", "Revenue (rolling)", df, False)

        with cR:
            if use_plotly and len(t) >= 2:
                fig = _build_plotly_line(go, t, risk, "Risk")
                _render_chart_card("Last updates", "Risk score (rolling)", fig, True)
            else:
                import pandas as pd
                df = pd.DataFrame({"Risk": risk}, index=t) if t else pd.DataFrame({"Risk": []})
                _render_chart_card("Last updates", "Risk score (rolling)", df, False)

    # Fragmented updater (best case: only KPIs + charts rerender)
    if fragment:
        @st.fragment(run_every=f"{REFRESH_SECONDS}s")
        def live_panel():
            if st.session_state.live_on:
                st.session_state.current_data = _apply_drift(st.session_state.current_data)

                kpis = _calc_kpis(st.session_state.current_data)

                # Append series (sync KPI + chart)
                now_label = datetime.now().strftime("%H:%M:%S")
                st.session_state.series["t"].append(now_label)
                st.session_state.series["revenue"].append(kpis["total_rev_7d"])
                st.session_state.series["risk"].append(kpis["risk_score"])

                # Trim
                for key in ("t", "revenue", "risk"):
                    if len(st.session_state.series[key]) > MAX_POINTS:
                        st.session_state.series[key] = st.session_state.series[key][-MAX_POINTS:]

            # Render KPI row + charts
            kpis_now = _calc_kpis(st.session_state.current_data)
            _render_kpi_row(kpis_now)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            _render_charts()

        live_panel()

    else:
        # Fallback: Streamlit version without fragments.
        # It will still work, but KPIs/charts rerun with the page.
        kpis_now = _calc_kpis(st.session_state.current_data)
        _render_kpi_row(kpis_now)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        _render_charts()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Actions row (unchanged main feature)
    a1, a2, a3 = st.columns([1, 2, 1])
    with a2:
        if st.button("Refresh Data Feed", use_container_width=True):
            st.session_state.current_data = data_generator.generate_full_dataset()
            st.session_state.ai_analysis = ""
            st.rerun()

        if st.button("Analyze Cross-Domain Risks", use_container_width=True):
            with st.spinner("Synthesizing intelligence..."):
                st.session_state.ai_analysis = ai_engine.analyze_state(st.session_state.current_data)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Hybrid layout: AI Briefing + Status (unchanged)
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
        generated_at = st.session_state.current_data.get("generated_at", "—")
        model_name = getattr(ai_engine, "DEFAULT_MODEL", None)
        model_text = model_name if model_name else "Demo Mode"

        st.markdown(
            f"""
<div class="os-card">
  <div style="font-weight:850; font-size:0.95rem;">System</div>
  <div style="margin-top:10px" class="small-muted">Status: <b>ONLINE</b></div>
  <div class="small-muted">Updated: <b>{generated_at}</b></div>
  <div style="height:10px"></div>
  <div class="small-muted">Model: <b>{model_text}</b></div>
  <div style="height:10px"></div>
  <div class="small-muted">Live: <b>{"ON" if st.session_state.live_on else "OFF"}</b></div>
</div>
""",
            unsafe_allow_html=True
        )
