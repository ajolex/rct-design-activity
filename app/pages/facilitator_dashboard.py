"""
Facilitator Dashboard - Monitor team progress and provide guidance
Password protected page for workshop facilitators
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import APP_PASSWORD, COACHING_PROMPTS, SPRINT_CHECKLIST

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Facilitator Dashboard",
    page_icon="👨‍🏫",
    layout="wide",
)

def check_password():
    """Returns True if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == APP_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "🔒 Facilitator Password",
            type="password",
            on_change=password_entered,
            key="password",
            help="Enter the facilitator dashboard password to access this page"
        )
        st.info("💡 **Password:**Set by ADMIN**")
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "🔒 Facilitator Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("😕 Password incorrect. Please try again.")
        return False
    else:
        # Password correct
        return True


def main():
    """Main facilitator dashboard."""
    
    st.title("👨‍🏫 Facilitator Dashboard")
    
    # Password check
    if not check_password():
        st.stop()
    
    # Logout button
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()
    
    st.markdown("---")
    
    # Dashboard content
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "💡 Coaching Tips", "📋 Sprint Checklist"])
    
    with tab1:
        st.header("Workshop Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Teams", "Check main app sessions")
            st.caption("Monitor participant activity in the main app")
        
        with col2:
            if st.session_state.get("start_time"):
                elapsed = datetime.now() - st.session_state.start_time
                minutes = int(elapsed.total_seconds() / 60)
                st.metric("Workshop Duration", f"{minutes} min")
            else:
                st.metric("Workshop Duration", "Not started")
        
        with col3:
            st.metric("Total Steps", "6")
            st.caption("Design sprint structure")
        
        st.markdown("---")
        
        st.subheader("📝 Session Notes")
        facilitator_notes = st.text_area(
            "Your facilitator notes (local session only)",
            height=200,
            placeholder="Track observations, common questions, timing adjustments...",
            key="facilitator_notes"
        )
        
        st.markdown("---")
        
        st.subheader("🎴 Program Cards Reference")
        st.markdown("""
        - **Education: Bridge to Basics** - Literacy intervention in Malawi schools
        - **Health: Community Care Loop** - Maternal health postpartum visits
        - **Agriculture: Smart Water Boost** - Drip irrigation adoption in Malawi
        """)
    
    with tab2:
        st.header("💡 Coaching Prompts")
        st.markdown("""
        Use these prompts during gallery walks or when teams seem stuck:
        """)
        
        for i, prompt in enumerate(COACHING_PROMPTS, 1):
            with st.expander(f"Prompt {i}"):
                st.markdown(f"**{prompt}**")
                st.markdown("""
                **When to use:**
                - During gallery walk reviews
                - When teams are stuck on a step
                - To push critical thinking
                """)
        
        st.markdown("---")
        
        st.subheader("🎯 Common Challenges & Solutions")
        
        challenges = {
            "Teams rushing through steps": "Remind teams: quality over speed. Each step builds on the last.",
            "Confusion about randomization unit": "Ask: 'At what level will you assign treatment?' Use program card logistics.",
            "Vague primary outcomes": "Push for specificity: 'How exactly will you measure this?'",
            "Unrealistic timelines": "Reference the decision horizon in their program card.",
            "Theory of change gaps": "Use the 'riskiest assumption' prompt to identify weak links."
        }
        
        for challenge, solution in challenges.items():
            st.markdown(f"**❓ {challenge}**")
            st.info(solution)
            st.markdown("")
    
    with tab3:
        st.header("📋 Sprint Completion Checklist")
        st.markdown("""
        Use this checklist during final reviews or gallery walks:
        """)
        
        for item in SPRINT_CHECKLIST:
            st.checkbox(item, key=f"checklist_{item}")
        
        st.markdown("---")
        
        st.subheader("⏱️ Timing Guidelines")
        st.markdown("""
        **Recommended workshop schedule:**
        
        | Phase | Duration | Notes |
        |-------|----------|-------|
        | Introduction & Card Assignment | 5 min | Distribute program cards, form teams |
        | Design Sprint (6 steps) | 18 min | 3 minutes per step |
        | Randomization Practice | 10 min | Use embedded tool with sample data |
        | Gallery Walk | 10 min | Teams review each other's designs |
        | Report Generation | 5 min | Export and review final designs |
        | Debrief | 10 min | Discuss learnings and next steps |
        | **Total** | **~60 min** | Adjust based on group size |
        """)
        
        st.markdown("---")
        
        st.subheader("🚀 Facilitation Tips")
        st.markdown("""
        1. **Start with energy** - Frame the workshop as a sprint, not a seminar
        2. **Enforce timing** - Use visible timer, give 1-minute warnings
        3. **Encourage peer learning** - Have teams share 1-2 key decisions
        4. **Focus on decisions** - Not perfect prose, but clear choices
        5. **Use the sample data** - Have teams download and try randomization
        6. **Celebrate completeness** - Recognize teams that finish all 6 steps
        7. **Capture questions** - Note common issues for future improvements
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.85rem; padding: 1rem 0;'>
        <p>👨‍🏫 Facilitator Dashboard • Access with ADMIN PASSWORD</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
