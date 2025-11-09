"""
RCT Design Activity: Main Streamlit App

An interactive workshop application for designing randomized controlled trials.
Participants work through a 6-step design sprint, from challenge framing through
decision triggers, using realistic program cards and sample data.
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    APP_TITLE, APP_SUBTITLE, APP_DESCRIPTION, CUSTOM_CSS,
    DEFAULT_SESSION_STATE, PARTICIPANT_GUIDANCE, SPRINT_CHECKLIST
)
from utils.program_cards import get_all_program_cards, get_program_card, format_card_for_display

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== CUSTOM STYLING =====
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


def initialize_session():
    """Initialize session state with defaults."""
    st.session_state.start_time = datetime.now()


def render_header():
    """Render app header with title and introduction."""
    st.markdown("<div class='main-title'>🎯 Design an RCT</div>", unsafe_allow_html=True)
    st.markdown(f"### {APP_SUBTITLE}")
    
    with st.expander("📖 About This Activity", expanded=False):
        st.markdown(APP_DESCRIPTION)
        st.markdown("---")
        st.markdown("**How to Use This Workbook:**")
        for i, guidance in enumerate(PARTICIPANT_GUIDANCE, 1):
            st.markdown(f"**{i}.** {guidance}")


def render_sidebar():
    """Render sidebar navigation and progress tracking."""
    with st.sidebar:
        st.header("📋 Workshop Navigation")
        
        # Team name input
        team_name = st.text_input(
            "👥 Team Name (required to start):",
            value=st.session_state.get("team_name", ""),
            key="team_name_input",
        )
        
        if team_name:
            st.session_state.team_name = team_name
            st.success(f"✓ Team: {team_name}")
        else:
            st.warning("⚠️ Please enter your team name to proceed")
            return False
        
        st.divider()
        
        # Program card selection
        st.subheader("🎴 Select Your Program Card")
        cards = get_all_program_cards()
        card_options = {card_id: card["title"] for card_id, card in cards.items()}
        
        selected_card_id = st.selectbox(
            "Choose your assigned program:",
            options=list(card_options.keys()),
            format_func=lambda x: card_options[x],
            key="card_select",
        )
        
        if selected_card_id:
            st.session_state.program_card_selected = selected_card_id
            card = get_program_card(selected_card_id)
            if card:
                st.info(f"📌 **{card['title']}**\n\n{card['sector']} • {card['theme']}")
        
        st.divider()
        
        # Progress tracking
        st.subheader("📊 Sprint Progress")
        completed_steps = len([k for k, v in st.session_state.responses.items() if v])
        total_steps = len(st.session_state.responses)
        progress = completed_steps / total_steps
        
        st.progress(progress)
        st.caption(f"**{completed_steps}/{total_steps}** steps completed")
        
        st.divider()
        
        # Quick links
        st.subheader("🔗 Quick Links")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 View Program Card", use_container_width=True):
                st.session_state.current_step = 0
        
        with col2:
            if st.button("🎲 Randomize", use_container_width=True):
                st.switch_page("pages/randomization.py")
        
        with col3:
            if st.button("📊 Generate Report", use_container_width=True):
                st.switch_page("pages/report_generation.py")
        
        st.divider()
        
        # Timer
        if st.session_state.start_time:
            elapsed = datetime.now() - st.session_state.start_time
            minutes = int(elapsed.total_seconds() / 60)
            seconds = int(elapsed.total_seconds() % 60)
            st.caption(f"⏱️ Elapsed: {minutes}m {seconds}s")
        
        return True


def render_welcome_section():
    """Render welcome and introduction section."""
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🚀 Ready to Design Your RCT?
        
        This workshop will guide you through 6 key steps to turn your program concept into 
        a rigorous randomized controlled trial (RCT) design. You'll work as a team to:
        
        1. **Frame the Challenge** – Clarify your core problem and success vision
        2. **Map the Theory of Change** – Connect your activities to outcomes
        3. **Design Measurement** – Choose indicators and instruments
        4. **Plan Randomization** – Select your assignment approach
        5. **Safeguard Implementation** – Build operational rhythms and signals
        6. **Decide and Commit** – Record your decision trigger and next steps
        
        **Each section takes 3 minutes.** Work through in order, capture decisions, 
        and mark any items [ ] you'll revisit during the gallery walk.
        """)
        
        st.markdown("### ✅ Sprint Checklist")
        for item in SPRINT_CHECKLIST:
            st.markdown(f"- [ ] {item}")
    
    with col2:
        st.info("""
        ### 📍 Session Snapshot
        
        **Duration:** 30 min
        
        **Format:**
        - 4 min: Welcome
        - 18 min: Design Sprint
        - 5 min: Gallery
        - 3 min: Commit
        
        **Deliverables:**
        - Theory of Change
        - Measurement Plan
        - Randomization Design
        - Decision Trigger
        """)


def main():
    """Main app entry point."""
    
    # Check sidebar for team name
    if not render_sidebar():
        st.error("⚠️ Please enter your team name in the sidebar to begin.")
        st.stop()
    
    # Render main header
    render_header()
    
    # Check if team has selected a program card
    if not st.session_state.program_card_selected:
        st.warning("👈 Please select your program card in the sidebar to proceed.")
        render_welcome_section()
        st.stop()
    
    # Main navigation based on current_step
    current_step = st.session_state.get("current_step", 1)
    
    if current_step == 0:
        # Program card display page
        st.markdown("---")
        render_program_card_display()
    
    elif current_step == 1:
        render_welcome_section()
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start Design Sprint", use_container_width=True, key="start_sprint"):
                st.session_state.current_step = 2
                st.rerun()
        
        with col2:
            if st.button("📄 View Program Card", use_container_width=True):
                st.session_state.current_step = 0
                st.rerun()
    
    else:
        # Show design workbook steps
        render_design_workbook()


def render_design_workbook():
    """Render the design workbook steps interface."""
    st.markdown("---")
    st.header("📝 RCT Design Workbook")
    
    st.markdown("""
    ### Work Through the Design Steps
    
    Now that you've selected your program, work through the following design considerations:
    """)
    
    # Design steps checklist
    steps = [
        ("1. Frame the Challenge", "Define your research question and key outcomes"),
        ("2. Map Theory of Change", "Connect activities to expected outcomes"),
        ("3. Design Measurement", "Select indicators and data collection methods"),
        ("4. Plan Randomization", "Choose randomization approach and unit"),
        ("5. Safeguard Implementation", "Identify risks and mitigation strategies"),
        ("6. Decide and Commit", "Define success criteria and decision triggers")
    ]
    
    for step_title, step_desc in steps:
        with st.expander(f"**{step_title}**"):
            st.markdown(f"_{step_desc}_")
            st.text_area(f"Notes for {step_title}", key=f"notes_{step_title}", height=100)
    
    st.markdown("---")
    st.success("✅ Once you've worked through the design steps, proceed to randomization!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Welcome", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    with col2:
        if st.button("📄 View Program Card", use_container_width=True):
            st.session_state.current_step = 0
            st.rerun()
    
    with col3:
        if st.button("Next: Randomization →", type="primary", use_container_width=True):
            st.switch_page("pages/randomization.py")


def render_program_card_display():
    """Render the selected program card in full detail."""
    card_id = st.session_state.program_card_selected
    card = get_program_card(card_id)
    
    if not card:
        st.error("Program card not found.")
        return
    
    formatted = format_card_for_display(card)
    
    # Header
    st.markdown(f"## 🎴 {formatted['title']}")
    st.markdown(f"**Sector:** {formatted['sector']} | **Theme:** {formatted['theme']}")
    
    st.divider()
    
    # Context section
    st.subheader("📍 Context Snapshot")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Problem**")
        st.write(formatted['context_sections'][0][1])
    
    with col2:
        st.markdown("**Resources**")
        st.write(formatted['context_sections'][1][1])
    
    with col3:
        st.markdown("**Logistics**")
        st.write(formatted['context_sections'][2][1])
    
    st.divider()
    
    # Program concept
    st.subheader("🎯 Program Concept")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Activities**")
        st.write(formatted['concept_sections'][0][1])
    
    with col2:
        st.markdown("**Approach**")
        st.write(formatted['concept_sections'][1][1])
    
    with col3:
        st.markdown("**Engagement**")
        st.write(formatted['concept_sections'][2][1])
    
    st.divider()
    
    # Decision horizon and metrics
    st.subheader("📊 Decision Horizon & Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Decision Trigger**")
        st.info(formatted['decision_horizon'])
    
    with col2:
        st.metric("Reach", formatted['reach'])
    
    with col3:
        st.metric("Budget", formatted['budget'])
    
    st.divider()
    
    # Considerations
    st.subheader("⚠️ Design Considerations")
    st.warning(formatted['considerations'])
    
    st.divider()
    
    # Baseline Data Download
    st.subheader("📊 Baseline Data for Randomization")
    
    # Map program card to data file
    data_file_map = {
        "education_bridge_to_basics": "data/sample_data/education_bridge_to_basics.csv",
        "health_community_care_loop": "data/sample_data/health_community_care_loop.csv",
        "agriculture_smart_water_boost": "data/sample_data/agriculture_smart_water_boost.csv"
    }
    
    if card_id in data_file_map:
        data_path = Path(data_file_map[card_id])
        
        if data_path.exists():
            import pandas as pd
            df = pd.read_csv(data_path)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"""
                **Sample Data Available:**
                - {len(df):,} records
                - {df.shape[1]} variables
                - Ready for randomization practice
                
                Download this baseline data to use with the RCT Field Flow randomization tool.
                """)
            
            with col2:
                # Download button
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Baseline Data",
                    data=csv_data,
                    file_name=data_path.name,
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Preview
            with st.expander("👁️ Preview Data (first 10 rows)"):
                st.dataframe(df.head(10), use_container_width=True)
        else:
            st.warning(f"Sample data file not found: {data_path}")
    
    st.divider()
    
    # Call to action
    st.success("✓ You've reviewed your program card. Ready to start the design sprint?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Begin Design Sprint", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    with col2:
        if st.button("← Back to Welcome", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()


if __name__ == "__main__":
    main()
