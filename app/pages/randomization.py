"""
Randomization page - Embedded RCT Field Flow randomization tool.
Provides interface for participants to randomize their designed experiments.
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="Randomization | RCT Design Activity",
    page_icon="🎲",
    layout="wide"
)

# Initialize session state
if "randomization_data" not in st.session_state:
    st.session_state.randomization_data = None
if "randomization_exported" not in st.session_state:
    st.session_state.randomization_exported = False


def display_instructions():
    """Display instructions for using the randomization tool."""
    st.markdown("""
    ### 🎲 Randomization - Assign Participants to Treatment Groups
    
    You've designed your RCT and created sample data. Now it's time to randomize 
    participant assignments to treatment and control groups.
    
    #### How to use the embedded randomization tool:
    
    1. **Choose Randomization Method**
       - **Simple**: Random assignment (50/50 by default)
       - **Stratified**: Random assignment within subgroups (e.g., by region, gender)
       - **Cluster**: Assignment at cluster level (e.g., schools, villages)
       - **Stratified + Cluster**: Combined approach
    
    2. **Set Parameters**
       - Treatment arms and proportions
       - Stratification variables (if applicable)
       - Seed for reproducibility
    
    3. **Run Randomization**
       - Balance checks automatically run
       - Download randomization code (Python/Stata)
       - Review results
    
    4. **Export Results**
       - Download the randomized dataset
       - Keep the seed for reproducibility
       - Save this for your final report
    
    #### Tips for Success:
    - **Use a seed** for reproducible results you can share with collaborators
    - **Check balance** across treatment groups for your key covariates
    - **Save the code** RCT Field Flow generates for transparency
    - **Document decisions** about randomization method and parameters
    """)


def display_embedded_app():
    """Display embedded RCT Field Flow randomization app."""
    st.markdown("---")
    st.markdown("### 📊 RCT Field Flow - Randomization Tool")
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("""
        **The randomization tool is embedded below.**
        
        Alternatively, you can open it in a new tab if the embedded view doesn't work:
        [🔗 Open RCT Field Flow](https://aj-rctfieldflow.streamlit.app/)
        """)
    
    with col2:
        if st.button("📖 Toggle Instructions", help="Show/hide detailed instructions"):
            st.session_state.show_randomization_help = not st.session_state.get("show_randomization_help", False)
    
    # Embed the RCT Field Flow app
    st.markdown(
        """
        <iframe 
            src="https://aj-rctfieldflow.streamlit.app/?embed=true"
            height="900"
            width="100%"
            frameborder="0"
            style="border-radius: 8px; border: 1px solid #ddd;"
        ></iframe>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")


def display_export_section():
    """Display section for exporting randomization results."""
    st.markdown("### 📥 Export Randomization Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Step 1: Download from RCT Field Flow**
        - Export your randomized dataset (CSV)
        - Save the randomization code
        - Note the random seed
        """)
    
    with col2:
        st.markdown("""
        **Step 2: Save Your Results**
        - Keep your exported CSV file
        - Include key columns: participant ID, treatment assignment
        - Optional: include balance covariates
        """)
    
    with col3:
        st.markdown("""
        **Step 3: Upload to Report**
        - Upload your randomization files in the Report Generation page
        - They will be included in your final report
        - Keep files for reproducibility
        """)
    
    st.markdown("---")
    st.info("""
    📌 **Next Step:** Upload your randomization files when you generate your final report on the Report Generation page.
    """)


def display_next_steps():
    """Display next steps after randomization."""
    if st.session_state.randomization_exported:
        st.markdown("---")
        st.markdown("### ✅ What's Next?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **For Your RCT Monitoring:**
            - Use randomization results to implement your intervention
            - Track treatment fidelity
            - Monitor participant engagement
            - Document any deviations from randomization
            """)
        
        with col2:
            st.markdown("""
            **For Your Final Report:**
            - Your randomization data and code are saved
            - Include randomization method in Methods section
            - Add balance table to report
            - Reference random seed for reproducibility
            """)
        
        st.markdown("---")
        st.markdown("### 📄 Ready to Generate Your Design Report?")
        
        if st.button("→ Go to Final Report", use_container_width=True):
            st.switch_page("pages/report_generation.py")


def main():
    """Main randomization page."""
    # Header
    st.title("🎲 Randomization & Treatment Assignment")
    
    # Display instructions
    display_instructions()
    
    # Embedded app
    display_embedded_app()
    
    # Export section
    display_export_section()
    
    # Next steps
    display_next_steps()
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Design", use_container_width=True):
            st.switch_page("app/main.py")
    
    with col3:
        if st.session_state.randomization_exported:
            if st.button("Continue to Report →", use_container_width=True):
                st.switch_page("pages/report_generation.py")


if __name__ == "__main__":
    main()
