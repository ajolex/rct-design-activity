"""Program card selection page."""

import streamlit as st
from pathlib import Path
from app.utils.program_cards import load_program_card, get_available_programs


def show_program_selection():
    """Display program card selection interface."""
    st.title("📋 Select Your Program Card")
    
    st.markdown("""
    Choose the program you've been assigned to evaluate. Each program card contains:
    - Program description and goals
    - Target population
    - Implementation details
    - Evaluation considerations
    """)
    
    # Get available program cards
    programs = get_available_programs()
    
    if not programs:
        st.error("⚠️ No program cards found. Please ensure program cards are in the `data/program_cards/` directory.")
        if st.button("← Back to Introduction"):
            st.session_state.page = "introduction"
            st.rerun()
        return
    
    # Program selection
    st.subheader("Available Programs")
    
    # Display programs in columns
    cols = st.columns(min(len(programs), 3))
    
    for idx, program in enumerate(programs):
        with cols[idx % 3]:
            program_name = program.replace('_', ' ').title()
            
            # Create a card-like container
            with st.container():
                st.markdown(f"### {program_name}")
                
                # Show preview/icon based on program type
                if 'education' in program.lower():
                    st.markdown("🎓 **Education Program**")
                elif 'health' in program.lower():
                    st.markdown("🏥 **Health Program**")
                elif 'agriculture' in program.lower():
                    st.markdown("🌾 **Agriculture Program**")
                else:
                    st.markdown("📊 **Development Program**")
                
                if st.button(f"Select {program_name}", key=f"select_{program}", use_container_width=True):
                    st.session_state.selected_program = program
                    st.session_state.page = "program_card_view"
                    st.rerun()
    
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "introduction"
            st.rerun()


def show_program_card_view():
    """Display the selected program card content."""
    if 'selected_program' not in st.session_state:
        st.error("No program selected. Please select a program first.")
        if st.button("← Back to Selection"):
            st.session_state.page = "program_selection"
            st.rerun()
        return
    
    program = st.session_state.selected_program
    program_name = program.replace('_', ' ').title()
    
    st.title(f"📋 {program_name}")
    
    # Load and display program card
    card_content = load_program_card(program)
    
    if card_content:
        # Display the markdown content
        st.markdown(card_content)
    else:
        st.error(f"Could not load program card: {program}")
        if st.button("← Back to Selection"):
            st.session_state.page = "program_selection"
            st.rerun()
        return
    
    st.markdown("---")
    
    # Reading confirmation
    st.subheader("✅ Confirm Understanding")
    
    st.markdown("""
    Before proceeding to the design activity, make sure you understand:
    - The program's goals and activities
    - The target population
    - Implementation constraints
    - Key evaluation considerations
    """)
    
    confirm = st.checkbox(
        "I have read and understood the program card",
        key="program_card_confirmed"
    )
    
    # Navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "program_selection"
            st.rerun()
    
    with col3:
        if st.button("Next →", type="primary", disabled=not confirm, use_container_width=True):
            st.session_state.page = "design_workbook"
            st.rerun()
    
    if not confirm:
        st.info("👆 Please confirm you've read the program card to continue.")
