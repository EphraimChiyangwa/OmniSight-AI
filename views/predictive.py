import streamlit as st

def show(current_data, ai_engine):
    """Displays the Predictive Analytics view."""
    st.markdown("## 🔮 Future State Prediction")
    st.markdown("Forecast business impact based on current live patterns.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Configuration")
        timeframe = st.selectbox("Time Horizon", ["7 Days", "30 Days", "Quarterly"])
        
        # Button to trigger prediction
        if st.button("▶ Run Forecast", use_container_width=True):
            with st.spinner("Calculating probabilities..."):
                st.session_state.prediction = ai_engine.predict_future_state(current_data, timeframe)
    
    with col2:
        st.markdown("### Forecast Results")
        if st.session_state.prediction:
            st.markdown(f'<div class="analysis-container">{st.session_state.prediction}</div>', unsafe_allow_html=True)
        else:
            st.markdown("<div class='metric-card' style='text-align: center; color: #a0aec0;'>Select timeframe and run forecast.</div>", unsafe_allow_html=True)