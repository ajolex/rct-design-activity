"""
Randomization page - Embedded RCT Field Flow randomization tool.
Provides interface for participants to randomize their designed experiments.
"""

import streamlit as st
from datetime import datetime
import pandas as pd

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
        **Step 2: Upload Results**
        - Upload your exported CSV file below
        - Include key columns: participant ID, treatment assignment
        - Optional: include balance covariates
        """)
    
    with col3:
        st.markdown("""
        **Step 3: Verify & Save**
        - Review the randomization summary
        - Store for final report
        - Track for reproducibility
        """)
    
    st.markdown("---")
    st.markdown("#### 📤 Upload Your Randomization Results")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload randomized dataset (CSV)",
        type=["csv"],
        help="This should be the randomized data exported from RCT Field Flow"
    )
    
    if uploaded_file is not None:
        # Read the uploaded file
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.randomization_data = df
            st.session_state.randomization_exported = True
            
            # Display summary
            st.success("✅ Randomization data loaded successfully!")
            
            # Create tabs for viewing results
            tab1, tab2, tab3 = st.tabs(["📊 Summary", "📋 Data Preview", "📈 Balance Check"])
            
            with tab1:
                st.markdown("#### Randomization Summary")
                
                # Display basic info
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Total Participants", len(df))
                with cols[1]:
                    treatment_col = next((col for col in df.columns if 'treatment' in col.lower()), None)
                    if treatment_col:
                        st.metric("Treatment Columns Found", df[treatment_col].nunique())
                with cols[2]:
                    st.metric("Rows", len(df))
                
                # Treatment distribution
                if treatment_col:
                    st.markdown("##### Treatment Distribution")
                    dist = df[treatment_col].value_counts()
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.dataframe(dist, use_container_width=True)
                    with col2:
                        st.bar_chart(dist)
            
            with tab2:
                st.markdown("#### Data Preview")
                st.dataframe(df, use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Randomization Data",
                    data=csv,
                    file_name=f"randomization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with tab3:
                st.markdown("#### Balance Check Summary")
                
                # Display column statistics for balance assessment
                st.markdown("**Numeric Columns Summary Statistics**")
                numeric_cols = df.select_dtypes(include=['number']).columns
                
                if len(numeric_cols) > 0:
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                else:
                    st.info("No numeric columns found for balance analysis")
                
                # Treatment-specific analysis if available
                if treatment_col:
                    st.markdown(f"**Summary by {treatment_col}**")
                    for col in numeric_cols:
                        if col != treatment_col:
                            st.markdown(f"**{col}**")
                            summary = df.groupby(treatment_col)[col].describe()
                            st.dataframe(summary, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.session_state.randomization_exported = False


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
            st.switch_page("pages/design_workbook.py")
    
    with col3:
        if st.session_state.randomization_exported:
            if st.button("Continue to Report →", use_container_width=True):
                st.switch_page("pages/report_generation.py")


if __name__ == "__main__":
    main()
