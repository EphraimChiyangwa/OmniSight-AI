import streamlit as st

def show(current_data, ai_engine):
    """Displays the Domain Deep Dive view."""
    st.markdown("## 📊 Domain Specific Intelligence")
    st.markdown("Inspect raw data streams and perform isolated domain analysis.")
    st.markdown("<div class='os-card' style='margin-bottom:14px;'><b>Page</b> <span class='small-muted'>• your existing content below</span></div>", unsafe_allow_html=True)

    domain = st.selectbox("Select Domain Layer", list(current_data.keys()))
    
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown(f"### Raw Data Stream: {domain.title()}")
        st.json(current_data[domain][:3]) 

    with col_r:
        st.markdown(f"### AI Layer Analysis: {domain.title()}")
        if st.button(f"Analyze {domain} Only", use_container_width=True):
             with st.spinner(f"Analyzing {domain}..."):
                 analysis = ai_engine.analyze_specific_domain(domain, current_data[domain])
                 st.markdown(f'<div class="analysis-container">{analysis}</div>', unsafe_allow_html=True)