"""Introduction page for the RCT Design Activity."""

import streamlit as st
from app.config import AppConfig


def show_introduction():
    """Display the introduction page with activity overview."""
    st.title("🎓 RCT Design Training Activity")
    
    st.markdown("""
    ## Welcome to the RCT Design Workshop!
    
    This interactive application will guide you through designing a **Randomized Controlled Trial (RCT)** 
    for a development program. You'll work through the complete process from understanding your program 
    to creating a comprehensive evaluation design.
    """)
    
    # Activity Overview
    st.header("📋 Activity Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What You'll Do:
        1. **Select a Program Card** - Choose your assigned program to evaluate
        2. **Define Research Questions** - Identify what you want to learn
        3. **Design Your Study** - Plan sample, treatment, and control groups
        4. **Run Randomization** - Use our built-in tool to assign treatments
        5. **Generate Report** - Export your complete design plan
        """)
    
    with col2:
        st.markdown("""
        ### Learning Objectives:
        - Understand RCT fundamentals
        - Practice research design
        - Apply randomization techniques
        - Document evaluation plans
        - Think through practical implementation
        """)
    
    # Time Estimate
    st.info("⏱️ **Estimated Time:** 45-60 minutes")
    
    # Instructions
    st.header("📝 Instructions")
    
    st.markdown("""
    ### Getting Started:
    
    1. **Read your program card carefully** - Understand the program context, goals, and constraints
    2. **Follow the design workbook steps** - Each section builds on the previous one
    3. **Use the randomization tool** - Test your design with sample data
    4. **Save your work** - The app will track your progress through each step
    5. **Generate your report** - Export your complete design plan at the end
    
    ### Tips for Success:
    - 💡 Take time to think through each design decision
    - 🤝 Discuss with your group if working in teams
    - 📊 Consider practical constraints (budget, timeline, ethics)
    - ✅ Review your answers before moving to the next step
    - 🔄 You can go back and revise earlier sections if needed
    """)
    
    # What is an RCT?
    with st.expander("❓ What is a Randomized Controlled Trial (RCT)?"):
        st.markdown("""
        An **RCT** is the gold standard for measuring program impact. Key features:
        
        - **Random Assignment**: Participants are randomly assigned to treatment or control groups
        - **Control Group**: Comparison group that doesn't receive the intervention
        - **Treatment Group**: Receives the program intervention
        - **Baseline & Endline**: Data collection before and after intervention
        - **Causal Inference**: Random assignment enables us to estimate causal effects
        
        RCTs help answer: *"What would have happened to participants without the program?"*
        """)
    
    # About the Randomization Tool
    with st.expander("🔧 About the Randomization Tool"):
        st.markdown(f"""
        This app includes integration with the **RCT Field Flow** randomization tool:
        
        - Generate random treatment assignments
        - Handle stratification and blocking
        - Export randomization lists for field use
        - Ensure reproducible assignments
        
        📎 **External Tool**: [{AppConfig.RCT_FIELD_FLOW_URL}]({AppConfig.RCT_FIELD_FLOW_URL})
        
        You can use the embedded tool or visit the external site for more advanced features.
        """)
    
    st.markdown("---")
    
    # Ready to Start
    st.success("✨ **Ready to begin?** Click the button below to start your RCT design activity!")
    
    if st.button("🚀 Start Activity", type="primary", use_container_width=True):
        st.session_state.page = "program_selection"
        st.rerun()
    
    # Footer
    st.markdown("""
    ---
    *This training activity is designed to provide hands-on experience with RCT design. 
    For real-world applications, always consult with evaluation experts and follow ethical guidelines.*
    """)
