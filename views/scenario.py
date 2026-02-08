import streamlit as st

def show(current_data, ai_engine):
    """Displays the Scenario Modeling view."""
    st.markdown("## 🎭 Wargaming & Simulations")
    st.markdown("Select a predefined scenario to simulate cross-domain impact.")
    st.markdown("<div class='os-card' style='margin-bottom:14px;'><b>Page</b> <span class='small-muted'>• your existing content below</span></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    if c1.button("📉 Competitor Price Drop", use_container_width=True):
        with st.spinner("Simulating..."):
            st.session_state.scenario_result = ai_engine.simulate_scenario("Competitor drops price by 15%", current_data)
            
    if c2.button("🔥 Supply Chain Fail", use_container_width=True):
        with st.spinner("Simulating..."):
            st.session_state.scenario_result = ai_engine.simulate_scenario("Main Supplier goes bankrupt", current_data)
            
    if c3.button("🚀 Market Expansion", use_container_width=True):
        with st.spinner("Simulating..."):
            st.session_state.scenario_result = ai_engine.simulate_scenario("Expansion into EU Market", current_data)
            
    st.markdown("---")
    st.markdown("### Simulation Results")

    if st.session_state.scenario_result:
        st.markdown(f'<div class="analysis-container">{st.session_state.scenario_result}</div>', unsafe_allow_html=True)
    else:
         st.markdown("<div class='metric-card' style='text-align: center; color: #a0aec0;'>Awaiting scenario selection...</div>", unsafe_allow_html=True)