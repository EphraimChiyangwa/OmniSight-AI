import streamlit as st

def show(current_data, ai_engine):
    """Displays the main Executive Dashboard view."""
    st.markdown("## 🎯 Executive Intelligence Hub")
    
    # 1. Metrics Row Calculation
    total_rev = sum(d['amount'] for d in current_data['finance'][:7] if d['type'] == 'Income')
    active_ops = sum(1 for d in current_data['operations'] if d['status'] in ['Active', 'Degraded'])
    risk_partners = sum(1 for d in current_data['partners'] if d['relationship_health'] < 0.75)
    
    # Metrics Display
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Total Revenue", f"${total_rev:,.0f}", "+32.4% ↑", "delta-pos"),
        ("Active Ops", f"{active_ops} Lines", "Stable", "delta-pos"),
        ("Partner Risk", f"{risk_partners} Detected", "+12% ↑", "delta-neg"),
        ("Client Churn", "Low", "Stable", "delta-pos")
    ]
    
    for col, (lbl, val, delta, d_class) in zip([c1,c2,c3,c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">{lbl}</div>
                <div class="metric-val">{val}</div>
                <div class="metric-delta {d_class}">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
            
    # 2. AI Analysis Section
    st.markdown("<br>", unsafe_allow_html=True)
    # Uses use_container_width to span the full width
    if st.button("⚡ Analyze Cross-Domain Risks", use_container_width=True):
        with st.spinner("Synthesizing Intelligence..."):
            # Calls the AI engine and stores result in session state
            st.session_state.ai_analysis = ai_engine.analyze_state(current_data)
    
    # Display results if they exist in state
    if st.session_state.ai_analysis:
        st.markdown(f'<div class="analysis-container">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
    else:
        st.info("System Standby. Click 'Analyze' to scan for cross-domain causal risks.")

    # 3. Chat Section
    st.markdown("---")
    st.subheader("💬 Ask the Data")
    q = st.text_input("Query:", placeholder="e.g., Why is revenue dropping in APAC?", label_visibility="collapsed")
    if q:
        with st.spinner("Thinking..."):
            ans = ai_engine.ask_ai_question(q, current_data)
            st.markdown(f"**Insight:** {ans}")