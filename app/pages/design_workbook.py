"""RCT Design Workbook - Interactive design steps."""

import streamlit as st
from typing import Dict, Any


def initialize_design_data():
    """Initialize the design data structure in session state."""
    if 'design_data' not in st.session_state:
        st.session_state.design_data = {
            'research_question': '',
            'primary_outcome': '',
            'secondary_outcomes': [],
            'population': {
                'target': '',
                'eligibility': '',
                'sample_size': 0
            },
            'treatment': {
                'description': '',
                'duration': '',
                'delivery': ''
            },
            'control': {
                'type': '',
                'description': ''
            },
            'randomization': {
                'unit': '',
                'method': '',
                'stratification': ''
            },
            'timeline': {
                'baseline': '',
                'intervention': '',
                'endline': ''
            },
            'budget': '',
            'ethical_considerations': '',
            'implementation_challenges': ''
        }


def show_design_workbook():
    """Display the interactive RCT design workbook."""
    initialize_design_data()
    
    st.title("📝 RCT Design Workbook")
    
    program_name = st.session_state.get('selected_program', 'Program').replace('_', ' ').title()
    st.markdown(f"**Designing an RCT for:** {program_name}")
    
    # Progress tracker
    sections = [
        "Research Questions",
        "Population & Sample",
        "Treatment & Control",
        "Randomization",
        "Data Collection",
        "Implementation"
    ]
    
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 0
    
    # Progress bar
    progress = (st.session_state.current_section + 1) / len(sections)
    st.progress(progress)
    st.caption(f"Section {st.session_state.current_section + 1} of {len(sections)}")
    
    st.markdown("---")
    
    # Display current section
    current = st.session_state.current_section
    
    if current == 0:
        show_research_questions()
    elif current == 1:
        show_population_sample()
    elif current == 2:
        show_treatment_control()
    elif current == 3:
        show_randomization()
    elif current == 4:
        show_data_collection()
    elif current == 5:
        show_implementation()
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_section -= 1
                st.rerun()
        else:
            if st.button("← Back to Card", use_container_width=True):
                st.session_state.page = "program_card_view"
                st.rerun()
    
    with col3:
        if current < len(sections) - 1:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.current_section += 1
                st.rerun()
        else:
            if st.button("Continue to Randomization →", type="primary", use_container_width=True):
                st.session_state.page = "randomization"
                st.rerun()


def show_research_questions():
    """Section 1: Research Questions and Outcomes."""
    st.header("1️⃣ Research Questions and Outcomes")
    
    st.markdown("""
    Define what you want to learn from this evaluation. A good research question is:
    - **Specific**: Clear and focused
    - **Measurable**: Can be answered with data
    - **Relevant**: Important to stakeholders
    - **Feasible**: Can be answered within constraints
    """)
    
    # Research Question
    st.subheader("Primary Research Question")
    st.session_state.design_data['research_question'] = st.text_area(
        "What is the main question you want to answer?",
        value=st.session_state.design_data['research_question'],
        placeholder="Example: Does providing free textbooks improve student learning outcomes?",
        height=100,
        help="Frame as a causal question: Does X cause Y?"
    )
    
    # Primary Outcome
    st.subheader("Primary Outcome")
    st.session_state.design_data['primary_outcome'] = st.text_area(
        "What is your main outcome of interest?",
        value=st.session_state.design_data['primary_outcome'],
        placeholder="Example: Student test scores in mathematics and language",
        help="This should directly answer your research question"
    )
    
    # Secondary Outcomes
    st.subheader("Secondary Outcomes (Optional)")
    
    # Display existing secondary outcomes
    if st.session_state.design_data['secondary_outcomes']:
        for idx, outcome in enumerate(st.session_state.design_data['secondary_outcomes']):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"• {outcome}")
            with col2:
                if st.button("Remove", key=f"remove_outcome_{idx}"):
                    st.session_state.design_data['secondary_outcomes'].pop(idx)
                    st.rerun()
    
    # Add new secondary outcome
    new_outcome = st.text_input(
        "Add a secondary outcome",
        key="new_secondary_outcome",
        placeholder="Example: School attendance rates"
    )
    if st.button("Add Outcome") and new_outcome:
        st.session_state.design_data['secondary_outcomes'].append(new_outcome)
        st.rerun()
    
    with st.expander("💡 Tips for Defining Outcomes"):
        st.markdown("""
        - **Primary outcome**: The most important measure of success
        - **Secondary outcomes**: Additional benefits or effects
        - Make sure outcomes are:
          - Measurable with available data
          - Relevant to stakeholders
          - Likely to change within your timeline
        """)


def show_population_sample():
    """Section 2: Population and Sample."""
    st.header("2️⃣ Population and Sample")
    
    st.markdown("""
    Define who will participate in your study and how many participants you need.
    """)
    
    # Target Population
    st.subheader("Target Population")
    st.session_state.design_data['population']['target'] = st.text_area(
        "Describe the target population for this program",
        value=st.session_state.design_data['population']['target'],
        placeholder="Example: Primary school students in grades 3-5 in rural districts",
        help="Who is the program designed to benefit?"
    )
    
    # Eligibility Criteria
    st.subheader("Eligibility Criteria")
    st.session_state.design_data['population']['eligibility'] = st.text_area(
        "What are the inclusion/exclusion criteria?",
        value=st.session_state.design_data['population']['eligibility'],
        placeholder="Example: Include students enrolled in public schools; Exclude students in boarding schools",
        help="Be specific about who can and cannot participate"
    )
    
    # Sample Size
    st.subheader("Sample Size")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.design_data['population']['sample_size'] = st.number_input(
            "Estimated total sample size",
            min_value=0,
            value=st.session_state.design_data['population']['sample_size'],
            help="Total number of units (individuals, schools, villages, etc.)"
        )
    
    with col2:
        if st.session_state.design_data['population']['sample_size'] > 0:
            treatment_pct = st.slider(
                "Percent assigned to treatment",
                min_value=10,
                max_value=90,
                value=50,
                step=5,
                help="Common: 50% treatment, 50% control"
            )
            n_treatment = int(st.session_state.design_data['population']['sample_size'] * treatment_pct / 100)
            n_control = st.session_state.design_data['population']['sample_size'] - n_treatment
            st.info(f"**Treatment group:** {n_treatment}  \n**Control group:** {n_control}")
    
    with st.expander("💡 Tips for Sample Size"):
        st.markdown("""
        Consider:
        - **Power analysis**: How many participants do you need to detect an effect?
        - **Attrition**: Add 10-20% extra to account for dropout
        - **Budget**: Can you afford to survey and track this many participants?
        - **Clustering**: If randomizing at group level (schools, villages), need more units
        """)


def show_treatment_control():
    """Section 3: Treatment and Control Groups."""
    st.header("3️⃣ Treatment and Control Groups")
    
    # Treatment Group
    st.subheader("Treatment Group")
    st.markdown("Describe what the treatment group will receive.")
    
    st.session_state.design_data['treatment']['description'] = st.text_area(
        "Treatment description",
        value=st.session_state.design_data['treatment']['description'],
        placeholder="Example: Free textbooks for mathematics and language, delivered at start of school year",
        help="What exactly will participants in the treatment group receive?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.design_data['treatment']['duration'] = st.text_input(
            "Treatment duration",
            value=st.session_state.design_data['treatment']['duration'],
            placeholder="Example: Full academic year (9 months)"
        )
    
    with col2:
        st.session_state.design_data['treatment']['delivery'] = st.text_input(
            "Delivery method",
            value=st.session_state.design_data['treatment']['delivery'],
            placeholder="Example: Distributed by teachers in classroom"
        )
    
    # Control Group
    st.subheader("Control Group")
    
    control_type = st.radio(
        "Type of control group",
        options=[
            "Pure control (nothing)",
            "Comparison (alternative treatment)",
            "Delayed treatment (wait list)",
            "Standard care (business as usual)"
        ],
        help="What will the control group receive?"
    )
    st.session_state.design_data['control']['type'] = control_type
    
    st.session_state.design_data['control']['description'] = st.text_area(
        "Control group description",
        value=st.session_state.design_data['control']['description'],
        placeholder="Example: Continue with regular instruction using existing textbooks",
        help="Describe what the control group experiences"
    )
    
    with st.expander("💡 Ethical Considerations for Control Groups"):
        st.markdown("""
        - **Pure control**: Denying treatment may raise ethical concerns if benefits are clear
        - **Delayed treatment**: Offering treatment later can be more ethical
        - **Standard care**: Compare new program to existing services
        - **Comparison**: Test which approach works better
        
        Always consider:
        - Will control group be harmed?
        - Can you justify withholding treatment?
        - Can you offer treatment to control group later?
        """)


def show_randomization():
    """Section 4: Randomization Strategy."""
    st.header("4️⃣ Randomization Strategy")
    
    st.markdown("""
    Plan how you will randomly assign participants to treatment and control groups.
    """)
    
    # Unit of Randomization
    st.subheader("Unit of Randomization")
    unit = st.radio(
        "What is the unit of randomization?",
        options=[
            "Individual (person)",
            "Household (family)",
            "Group (school, village, clinic, etc.)",
            "Other"
        ],
        help="At what level will you assign treatment?"
    )
    
    if unit == "Other":
        unit = st.text_input("Specify unit:", placeholder="Example: Agricultural plots")
    
    st.session_state.design_data['randomization']['unit'] = unit
    
    # Randomization Method
    st.subheader("Randomization Method")
    method = st.radio(
        "What randomization method will you use?",
        options=[
            "Simple randomization (like flipping a coin)",
            "Block randomization (equal groups)",
            "Stratified randomization (balance on characteristics)",
            "Cluster randomization (assign groups together)"
        ],
        help="How will you ensure fair assignment?"
    )
    st.session_state.design_data['randomization']['method'] = method
    
    # Stratification
    if "Stratified" in method or "Block" in method:
        st.subheader("Stratification Variables")
        st.session_state.design_data['randomization']['stratification'] = st.text_area(
            "Which variables will you stratify on?",
            value=st.session_state.design_data['randomization']['stratification'],
            placeholder="Example: School size (small/large), District, Baseline test scores",
            help="Stratifying ensures balance on important characteristics"
        )
    
    with st.expander("💡 Understanding Randomization Methods"):
        st.markdown("""
        - **Simple**: Assign each unit independently (like coin flip)
          - *Pros*: Easy, truly random
          - *Cons*: May result in unequal group sizes
        
        - **Block**: Ensure equal group sizes in blocks
          - *Pros*: Balanced groups
          - *Cons*: Slightly more complex
        
        - **Stratified**: Randomize separately within strata
          - *Pros*: Ensures balance on key characteristics
          - *Cons*: Need to define strata in advance
        
        - **Cluster**: Assign entire groups (schools, villages)
          - *Pros*: Avoids contamination, easier logistics
          - *Cons*: Need more clusters, reduced power
        """)


def show_data_collection():
    """Section 5: Data Collection Timeline."""
    st.header("5️⃣ Data Collection Timeline")
    
    st.markdown("""
    Plan when you will collect data to measure outcomes.
    """)
    
    # Timeline diagram
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Baseline")
        st.session_state.design_data['timeline']['baseline'] = st.text_area(
            "When and what?",
            value=st.session_state.design_data['timeline']['baseline'],
            placeholder="Example: Before school year starts. Measure: prior test scores, demographics",
            key="baseline_timeline",
            height=120
        )
    
    with col2:
        st.markdown("### 🎯 Intervention")
        st.session_state.design_data['timeline']['intervention'] = st.text_area(
            "When and duration?",
            value=st.session_state.design_data['timeline']['intervention'],
            placeholder="Example: Throughout school year (9 months)",
            key="intervention_timeline",
            height=120
        )
    
    with col3:
        st.markdown("### 📈 Endline")
        st.session_state.design_data['timeline']['endline'] = st.text_area(
            "When and what?",
            value=st.session_state.design_data['timeline']['endline'],
            placeholder="Example: End of school year. Measure: final test scores, attendance",
            key="endline_timeline",
            height=120
        )
    
    # Budget Considerations
    st.subheader("Budget Estimate")
    st.session_state.design_data['budget'] = st.text_area(
        "Estimated budget and major cost categories",
        value=st.session_state.design_data['budget'],
        placeholder="Example: $50,000 total: Program delivery ($30k), Surveys ($15k), Staff ($5k)",
        help="Break down major expenses"
    )
    
    with st.expander("💡 Data Collection Tips"):
        st.markdown("""
        **Baseline (before treatment):**
        - Measure outcomes before intervention starts
        - Collect covariates for analysis and stratification
        - Verify eligibility and consent
        
        **Endline (after treatment):**
        - Measure same outcomes as baseline for comparison
        - Time gap should allow effects to emerge
        - Plan for follow-up surveys to track persistence
        
        **Budget considerations:**
        - Survey costs (enumerators, tablets, training)
        - Program delivery costs
        - Incentives for participation
        - Administrative and overhead
        """)


def show_implementation():
    """Section 6: Implementation and Ethics."""
    st.header("6️⃣ Implementation and Ethical Considerations")
    
    # Ethical Considerations
    st.subheader("Ethical Considerations")
    st.markdown("Address potential ethical issues in your design.")
    
    st.session_state.design_data['ethical_considerations'] = st.text_area(
        "How will you address ethical concerns?",
        value=st.session_state.design_data['ethical_considerations'],
        placeholder="Example: Obtain informed consent, protect privacy, offer treatment to control group after study ends",
        height=120,
        help="Consider: consent, privacy, fairness, potential harms"
    )
    
    ethical_checklist = st.multiselect(
        "Ethical safeguards (check all that apply)",
        options=[
            "Informed consent from participants",
            "IRB/Ethics committee approval",
            "Data privacy protections",
            "Minimize harm to control group",
            "Fair compensation for participation",
            "Plan to share results with community"
        ]
    )
    
    # Implementation Challenges
    st.subheader("Implementation Challenges")
    st.markdown("Anticipate practical challenges and how you'll address them.")
    
    st.session_state.design_data['implementation_challenges'] = st.text_area(
        "What challenges do you anticipate and how will you address them?",
        value=st.session_state.design_data['implementation_challenges'],
        placeholder="Example: Challenge - Low survey response rate. Solution - Offer small incentives and multiple contact attempts",
        height=150,
        help="Think about logistics, compliance, attrition, contamination"
    )
    
    common_challenges = st.multiselect(
        "Common challenges to consider",
        options=[
            "Attrition (participants dropping out)",
            "Non-compliance (not taking treatment)",
            "Contamination (control group gets treatment)",
            "Spillover effects (treatment affects control)",
            "Data quality issues",
            "Budget constraints",
            "Political or stakeholder resistance"
        ]
    )
    
    with st.expander("💡 Planning for Success"):
        st.markdown("""
        **Ethical best practices:**
        - Always obtain informed consent
        - Protect participant privacy and confidentiality
        - Minimize risks to participants
        - Ensure fair selection of participants
        - Plan to share findings with community
        
        **Implementation tips:**
        - Build in extra time and budget
        - Train staff thoroughly
        - Pilot test procedures
        - Monitor implementation closely
        - Have contingency plans
        - Maintain regular communication with stakeholders
        """)
    
    st.success("✅ You've completed the design workbook! Next, you can test your randomization strategy.")
