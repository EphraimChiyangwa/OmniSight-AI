from pathlib import Path
from datetime import datetime
from time import time
import random

import streamlit as st
import streamlit.components.v1 as components

import data_generator

REFRESH_SECONDS = 5
MAX_POINTS = 60


def _logo_path():
    here = Path(__file__).resolve().parent
    root = here.parent
    p = root / "image" / "OmniSightLogo.png"
    return str(p) if p.exists() else None


def _inject_chart_css():
    st.markdown(
        """
<style>
.os-chart-card{
  width: 100%;
  border-radius: 16px;
  background: linear-gradient(133.84deg, #4E4E4E -16.04%, #333333 9.33%, #1A1A1A 32.02%, #1A1A1A 62.06%, #262626 87.42%, #4E4E4E 112.12%);
  box-shadow: 2px 6px 15px 2px rgba(12, 10, 11, 0.8);
  border: 1px solid rgba(255,255,255,0.08);
  overflow: hidden;
}

.os-chart-head{
  padding: 12px 16px;
  display:flex;
  align-items:center;
  justify-content:space-between;
}

.os-chart-divider{
  height: 1px;
  width: 100%;
  background: rgba(255,255,255,0.20);
}

.os-chart-title .h6{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  font-weight: 700;
  font-size: 18px;
  line-height: 24px;
  color:#FFFFFF !important;
}

.os-chart-title .sub{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  font-weight: 400;
  font-size: 13px;
  line-height: 18px;
  color: rgba(217,217,217,0.90) !important;
}

.os-chart-body{
  padding: 10px 12px 12px 12px;
}

.os-chart-note{
  margin-top: 6px;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  font-size: 12px;
  line-height: 16px;
  color: rgba(217,217,217,0.82);
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _init_live_state():
    if "live_on" not in st.session_state:
        st.session_state.live_on = True
    if "series" not in st.session_state:
        st.session_state.series = {"t": [], "revenue": [], "risk": []}
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = ""
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = None
    if "last_tick_ts" not in st.session_state:
        st.session_state.last_tick_ts = time()  # start now (prevents weird countdown)
    if "next_update_in" not in st.session_state:
        st.session_state.next_update_in = REFRESH_SECONDS


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
    finance = current_data.get("finance", [])
    clients = current_data.get("clients", [])
    compliance = current_data.get("compliance", [])

    rev_mult = 1.0 + random.uniform(-0.015, 0.015)
    for t in finance[:30]:
        if isinstance(t, dict) and t.get("type") == "Income":
            amt = t.get("amount", 0)
            if isinstance(amt, (int, float)):
                t["amount"] = max(0.0, amt * rev_mult)

    churn_shift = random.uniform(-0.01, 0.02)
    for c in clients[:100]:
        if isinstance(c, dict):
            r = c.get("churn_risk", 0.0)
            if isinstance(r, (int, float)):
                c["churn_risk"] = min(max(r + churn_shift, 0.0), 1.0)

    comp_shift = random.uniform(-0.01, 0.01)
    for x in compliance[:80]:
        if isinstance(x, dict):
            cs = x.get("compliance_score", 1.0)
            if isinstance(cs, (int, float)):
                x["compliance_score"] = min(max(cs + comp_shift, 0.0), 1.0)

    current_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_data


def _try_plotly():
    try:
        import plotly.graph_objects as go
        return go
    except Exception:
        return None


def _render_chart_card(title, subtitle, fig_or_df, use_plotly: bool, note: str | None = None):
    st.markdown(
        """
<div class="os-chart-card">
  <div class="os-chart-head">
    <div class="os-chart-title">
      <div class="h6">{}</div>
      <div class="sub">{}</div>
    </div>
  </div>
  <div class="os-chart-divider"></div>
  <div class="os-chart-body">
        """.format(title, subtitle),
        unsafe_allow_html=True,
    )

    if use_plotly:
        fig_html = fig_or_df.to_html(
            full_html=False,
            include_plotlyjs="cdn",
            config={"displayModeBar": False, "responsive": True},
        )
        components.html(fig_html, height=270, scrolling=False)
    else:
        st.line_chart(fig_or_df, use_container_width=True)

    if note:
        st.markdown(f"<div class='os-chart-note'>{note}</div>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


def _build_plotly_line(go, x, y, name):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=3, color="#9290FE"),
            name=name,
            hovertemplate="%{y:.3s}<extra></extra>",
        )
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(229,231,235,0.88)"),
        showlegend=False,
        height=250,
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        zeroline=False,
        showticklabels=False,
        ticks="",
        fixedrange=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.10)",
        zeroline=False,
        showticklabels=True,
        tickfont=dict(size=11),
        tickformat="~s",
        nticks=4,
        fixedrange=True,
    )

    return fig


def show(current_data, ai_engine):
    _inject_chart_css()
    _init_live_state()

    if "current_data" not in st.session_state or not isinstance(st.session_state.current_data, dict):
        st.session_state.current_data = current_data

    logo = _logo_path()
    if logo:
        c1, c2, c3 = st.columns([1.2, 1, 1.2])
        with c2:
            st.image(logo, width=320)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    ctrl1, ctrl2 = st.columns([3, 1])
    with ctrl1:
        st.session_state.live_on = st.toggle("Live Mode", value=st.session_state.live_on)
        last = st.session_state.last_refresh

        if st.session_state.live_on:
            now_ts = time()
            elapsed = now_ts - st.session_state.last_tick_ts
            remaining = max(0, int(REFRESH_SECONDS - elapsed))
            st.session_state.next_update_in = remaining

            if last:
                st.markdown(
                    f"<div class='small-muted' style='margin-top:-6px;'>"
                    f"Live • Updates every <b>{REFRESH_SECONDS}s</b> • Next update in: <b>{remaining}s</b> • "
                    f"Last refreshed: <b>{last}</b></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='small-muted' style='margin-top:-6px;'>"
                    f"Live • Updates every <b>{REFRESH_SECONDS}s</b> • Next update in: <b>{remaining}s</b></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div class='small-muted' style='margin-top:-6px;'>Live mode is off</div>",
                unsafe_allow_html=True,
            )

    with ctrl2:
        if st.button("Reset Dataset", use_container_width=True):
            st.session_state.current_data = data_generator.generate_full_dataset()
            st.session_state.series = {"t": [], "revenue": [], "risk": []}
            st.session_state.ai_analysis = ""
            st.session_state.last_refresh = None
            st.session_state.last_tick_ts = time()
            st.session_state.next_update_in = REFRESH_SECONDS
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

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
                    unsafe_allow_html=True,
                )

        s = st.session_state.series
        rev_delta = "stable"
        risk_delta = "stable"

        if len(s["revenue"]) >= 2:
            rev_delta = "up" if s["revenue"][-1] >= s["revenue"][-2] else "down"
        if len(s["risk"]) >= 2:
            risk_delta = "up" if s["risk"][-1] >= s["risk"][-2] else "down"

        kpi(
            k1, "Revenue (7d)", f"${kpis['total_rev_7d']:,.0f}", rev_delta,
            "delta-pos" if rev_delta == "up" else ("delta-neg" if rev_delta == "down" else "delta-neutral"),
        )
        kpi(k2, "Production", f"{kpis['active_lines']} lines", "stable", "delta-neutral")
        kpi(k3, "Partners", f"{kpis['reliable_partners']}/{kpis['partners_total']}", "watch", "delta-neg")
        kpi(k4, "Clients", f"{kpis['active_clients']}", "ok", "delta-neutral")
        kpi(
            k5, "Risk Score", f"{kpis['risk_score']:.2f}", risk_delta,
            "delta-neg" if risk_delta == "up" else ("delta-pos" if risk_delta == "down" else "delta-neutral"),
        )

    def _render_charts():
        t = st.session_state.series["t"]
        rev = st.session_state.series["revenue"]
        risk = st.session_state.series["risk"]

        go = _try_plotly()
        use_plotly = go is not None

        cL, cR = st.columns(2)
        with cL:
            if use_plotly and len(t) >= 2:
                fig = _build_plotly_line(go, t, rev, "Revenue")
                _render_chart_card("Signal timeline", "Revenue (5s cadence)", fig, True)
            else:
                import pandas as pd
                df = pd.DataFrame({"Revenue": rev}, index=t) if t else pd.DataFrame({"Revenue": []})
                _render_chart_card("Signal timeline", "Revenue (5s cadence)", df, False)

        with cR:
            note = "Risk score blends churn + compliance — spikes signal rising exposure."
            if use_plotly and len(t) >= 2:
                fig = _build_plotly_line(go, t, risk, "Risk")
                _render_chart_card("Signal timeline", "Risk score (5s cadence)", fig, True, note=note)
            else:
                import pandas as pd
                df = pd.DataFrame({"Risk": risk}, index=t) if t else pd.DataFrame({"Risk": []})
                _render_chart_card("Signal timeline", "Risk score (5s cadence)", df, False, note=note)

    if fragment:
        @st.fragment(run_every="1s")
        def live_panel():
            if st.session_state.live_on:
                now_ts = time()
                if (now_ts - st.session_state.last_tick_ts) >= REFRESH_SECONDS:
                    st.session_state.last_tick_ts = now_ts

                    st.session_state.current_data = _apply_drift(st.session_state.current_data)
                    kpis = _calc_kpis(st.session_state.current_data)

                    now_label = datetime.now().strftime("%H:%M:%S")
                    st.session_state.last_refresh = now_label

                    st.session_state.series["t"].append(now_label)
                    st.session_state.series["revenue"].append(kpis["total_rev_7d"])
                    st.session_state.series["risk"].append(kpis["risk_score"])

                    for key in ("t", "revenue", "risk"):
                        if len(st.session_state.series[key]) > MAX_POINTS:
                            st.session_state.series[key] = st.session_state.series[key][-MAX_POINTS:]

            kpis_now = _calc_kpis(st.session_state.current_data)
            _render_kpi_row(kpis_now)
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            _render_charts()

        live_panel()
    else:
        kpis_now = _calc_kpis(st.session_state.current_data)
        _render_kpi_row(kpis_now)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        _render_charts()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    a1, a2, a3 = st.columns([1, 2, 1])
    with a2:
        if st.button("Analyze Cross-Domain Risks", use_container_width=True):
            with st.spinner("Synthesizing intelligence..."):
                st.session_state.ai_analysis = ai_engine.analyze_state(st.session_state.current_data)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    left, right = st.columns([3, 1])

    with left:
        if st.session_state.ai_analysis:
            st.markdown(f"<div class='os-brief'>{st.session_state.ai_analysis}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='os-brief'><span class='small-muted'>System ready.</span> Click <b>Analyze</b> to surface hidden cross-domain causes and impacts.</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='small-muted'>Ask the Data</div>", unsafe_allow_html=True)

        q = st.text_input("", placeholder="e.g. What triggered churn risk in APAC?", label_visibility="collapsed")
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
            unsafe_allow_html=True,
        )
