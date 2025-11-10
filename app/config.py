# Configuration and constants for the RCT Design Activity app

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# ===== APP METADATA =====
APP_TITLE = "Design an RCT: Interactive Workshop Activity"
APP_SUBTITLE = "Transform program concepts into rigorous randomized evaluations"
APP_DESCRIPTION = """
Work through a step-by-step design sprint to turn your program idea into a randomized controlled trial (RCT) design. 
This interactive workshop app guides your team from challenge/problem framing through evaluation planning to randomization 
and decision triggers. Use your assigned program card as the anchor, follow the workbook steps, use the realistic 
sample data, and export your final design plan as a design plan report.
"""

# ===== SESSION STATE DEFAULTS =====
DEFAULT_SESSION_STATE = {
    "team_name": "",
    "program_card_selected": None,
    "current_step": 1,
    "responses": {
        "frame_challenge": {},
        "theory_of_change": {},
        "measurement": {},
        "randomization": {},
        "implementation": {},
        "decision": {},
    },
    "sample_data_generated": False,
    "sample_data_file": None,
    "report_generated": False,
    "start_time": None,
}

# ===== PROGRAM CARDS =====
PROGRAM_CARDS = {
    "education_bridge_to_basics": {
        "title": "Education: Bridge to Basics",
        "sector": "Education",
        "theme": "Literacy",
        "context": {
            "problem": "Malawi district schools report shows that 55% of grade 4 students read below grade level.",
            "resources": "Municipal government can second 60 teachers for remedial instruction.",
            "logistics": "After-school slots available in 40 schools across three sub-provinces.",
        },
        "concept": {
            "activities": "Daily 45-minute literacy sessions in pull-out groups of 12 students.",
            "approach": "Tiered lesson plans aligned to foundational reading benchmarks.",
            "engagement": "SMS nudges sent to parents/guardians twice weekly with home practice tips.",
        },
        "decision_horizon": "School board requires evidence within two academic terms to renew funding.",
        "metrics": {
            "reach": "3,200 learners",
            "budget": "$180k",
        },
        "considerations": "Consider teacher capacity, parent engagement, and peer spillovers across classrooms.",
    },
    "health_community_care_loop": {
        "title": "Health: Community Care Loop",
        "sector": "Health",
        "theme": "Maternal Health",
        "context": {
            "problem": "Provincial report indicates a 30% drop in postpartum visit completion within six weeks.",
            "resources": "Partner NGO employs 120 community health workers covering 80 communities.",
            "logistics": "Electronic medical records system can flag missed visits daily.",
        },
        "concept": {
            "activities": "Health workers conduct two structured home visits focused on maternal recovery.",
            "approach": "Interactive voice response system delivers weekly health check-ins.",
            "engagement": "Clinic dashboards display real-time caseload and follow-up compliance.",
        },
        "decision_horizon": "Department of Health will expand region-wide if completion improves by 15 percentage points.",
        "metrics": {
            "reach": "6,400 mothers",
            "budget": "$240k",
        },
        "considerations": "Watch for contamination when health workers serve both treatment and control villages.",
    },
    "agriculture_smart_water_boost": {
        "title": "Agriculture: Smart Water Boost",
        "sector": "Agriculture",
        "theme": "Irrigation & Sustainability",
        "context": {
            "problem": "Malawian smallholder farmers face erratic rainfall and rising irrigation costs.",
            "resources": "Regional co-op offers subsidized drip irrigation kits but uptake stalls at 18%.",
            "logistics": "Satellite data partnership can provide parcel-level evapotranspiration estimates.",
        },
        "concept": {
            "activities": "Bundle drip kits with soil moisture sensors and advisory SMS on irrigation timing.",
            "approach": "Provide micro-leasing to spread hardware payments over two seasons.",
            "engagement": "Embed agronomist office hours at local co-op hubs twice per month.",
        },
        "decision_horizon": "Donor consortium will finance regional roll-out if net farm income rises by 12%.",
        "metrics": {
            "reach": "2,100 farms",
            "budget": "$310k",
        },
        "considerations": "Account for potential water spillovers and cooperative member influence on non-members.",
    },
}

# ===== WORKBOOK STEPS (from create_rct_booklet.py) =====
WORKBOOK_STEPS = [
    {
        "number": 1,
        "title": "Frame the Challenge",
        "goal": "Clarify the problem you are tackling and the change you want to see.",
        "actions": [
            "Review the program card and underline the core challenge.",
            "Note the primary participants and delivery setting.",
            "Write a one-sentence statement of success for the next 12 months.",
        ],
        "tip": "Keep your problem statement specific to one population and one outcome.",
        "fields": [
            {"key": "program_title", "label": "Program title", "type": "text"},
            {"key": "target_group", "label": "Target group", "type": "text", "placeholder": "e.g. Grade 4 students struggling with reading"},
            {"key": "delivery_setting", "label": "Delivery setting", "type": "text", "placeholder": "e.g. Facilitators lead biweekly sessions with female participants in school classrooms"},
            {"key": "success_statement", "label": "Success in 12 months looks like", "type": "textarea", "rows": 3, "placeholder": "e.g. 70% of participants move from below-grade-level to grade-level reading"},
        ],
    },
    {
        "number": 2,
        "title": "Map the Theory of Change",
        "goal": "Connect activities to outcomes so your randomization follows the logic.",
        "actions": [
            "List the major activities and the immediate outputs you can measure.",
            "Highlight the outcomes that must shift before your long-term impact appears.",
            "Flag assumptions that you're least confident about, that are most critical for success, or that are hardest to verify with data (e.g., spillovers, contamination, or behavioral changes).",
        ],
        "tip": "If you cannot draw a tight line from activity to outcome, consider narrowing scope.",
        "fields": [
            {"key": "riskiest_assumption", "label": "Riskiest assumption", "type": "textarea", "rows": 3, "placeholder": "e.g. We assume participants will attend 80% of sessions, but attendance could drop if sessions conflict with harvest season"},
            {"key": "early_signal", "label": "Early signal to watch", "type": "textarea", "rows": 3, "placeholder": "e.g. Within 2 months, 60% of participants should complete baseline assessments, showing engagement and buy-in"},
        ],
    },
    {
        "number": 3,
        "title": "Design Measurement",
        "goal": "Choose indicators and instruments that capture change credibly.",
        "actions": [
            "Lock one primary outcome and the metric you will use.",
            "Select instruments that are realistic for your team to field.",
            "Set timing for baseline and follow-up so you capture change.",
        ],
        "tip": "If an indicator feels fuzzy, add a quick definition or example in the notes.",
        "fields": [
            {"key": "primary_outcome_definition", "label": "Primary outcome definition", "type": "textarea", "rows": 3, "placeholder": "e.g. Students' reading proficiency measured by fluency assessment (words read correctly per minute); a score of 90+ WPM = grade level competency"},
            {"key": "instruments", "label": "Instrument(s)", "type": "textarea", "rows": 3, "placeholder": "e.g. Timed reading fluency test (1 min), comprehension quiz, classroom observations by trained assessors"},
            {"key": "baseline_timing", "label": "Baseline timing", "type": "text", "placeholder": "e.g. First 2 weeks of school year, before intervention starts"},
            {"key": "followup_timing", "label": "Follow-up timing", "type": "text", "placeholder": "e.g. End of school year (12 months), and mid-year check-in at 6 months"},
        ],
    },
    {
        "number": 4,
        "title": "Plan Randomization",
        "goal": "Select an assignment approach and sanity check for implementation.",
        "actions": [
            "Pick the level where you will randomize (individuals, villages, classrooms, clinics, etc.).",
            "List the steps to assign units and keep the process transparent.",
            "Anticipate spillovers or compliance risks and note how you will manage them.",
        ],
        "tip": "If spillovers feel unavoidable, consider cluster-level assignment.",
        "fields": [
            {"key": "randomization_unit", "label": "Randomization unit", "type": "text", "placeholder": "e.g. Individual students, School, Village, or Clinic"},
            {"key": "randomization_method", "label": "Method", "type": "text", "placeholder": "e.g. Simple random assignment (50/50 treatment/control), Stratified by gender, or Cluster-randomized by school"},
            {"key": "assignment_steps", "label": "Assignment steps and checks", "type": "textarea", "rows": 3, "placeholder": "e.g. 1) List all 320 eligible students, 2) Use RCT Field Flow tool to randomize, 3) School director seals envelope assignments, 4) Public announcement of groups"},
            {"key": "spillover_mitigation", "label": "Spillover mitigation", "type": "textarea", "rows": 3, "placeholder": "e.g. School-level randomization avoids students talking across groups; separate classrooms for treatment; clear communication that control group receives intervention later"},
        ],
    },
    {
        "number": 5,
        "title": "Safeguard Implementation",
        "goal": "Create systems and routines that help detect issues early and make informed adjustments without compromising the intervention’s integrity.",
        "actions": [
            "Establish mechanisms to ensure the intervention is delivered as planned..",
            "Capture logistics that could slow you down and draft mitigation steps.",
            "Data Quality and Progress Tracking: track key indicators and prevent data loss or quality issues",
        ],
        "tip": "Assign a lead person to each risk so follow-up happens quickly.",
        "fields": [
            {"key": "team_checkins", "label": "Team check-ins", "type": "textarea", "rows": 3, "placeholder": "e.g. Weekly meetings with implementers to review attendance, materials availability, and any challenges; monthly data quality audits"},
            {"key": "risks_to_watch", "label": "Risks to watch", "type": "textarea", "rows": 3, "placeholder": "e.g. Low attendance (trigger: >20% absence), staff turnover, equipment breakdown, participant dropout, changes in school policy"},
        ],
    },
    {
        "number": 6,
        "title": "Decide and Commit",
        "goal": "Moving from design to action by setting clear decision triggers and next steps.",
        "actions": [
            "Decide: Agree as a team on whether (and when) to proceed with the RCT as designed",
            "Commit: Formalize your next steps and responsibilities — who does what, by when — to move the design forward",
            "Decision checklist: Is the design feasible? Are partners and funding in place? Are ethical and logistical conditions ready?",
        ],
        "tip": "Be concrete: threshold, time frame, and decision owner.",
        "fields": [
            {"key": "decision_trigger", "label": "Decision trigger", "type": "textarea", "rows": 3, "placeholder": "e.g. If treatment group shows ≥25% improvement in reading scores vs. control group AND fidelity is ≥80%, proceed with scale-up by June 2025"},
            {"key": "stakeholders_to_brief", "label": "Stakeholders to brief", "type": "textarea", "rows": 3, "placeholder": "e.g. School board, district education office, implementing partner NGO, donor (Ministry of Education)"},
            {"key": "next_steps", "label": "Next steps after briefing", "type": "textarea", "rows": 3, "placeholder": "e.g. If positive: submit scale-up proposal, train 20 new facilitators, apply for expansion budget; if null/negative: conduct qualitative analysis to understand barriers"},
        ],
    },
]

# ===== RANDOMIZATION CONFIG =====
RCT_FIELD_FLOW_URL = "https://ajolex.github.io/rct_field_flow"
RCT_FIELD_FLOW_GITHUB = "https://github.com/ajolex/rct_field_flow"

# ===== REPORT CONFIG =====
REPORT_FORMATS = ["HTML", "PDF"]
REPORT_FILENAME_TEMPLATE = "{team_name}_{program_card}_{timestamp}.{ext}"

# ===== STYLING =====
CUSTOM_CSS = """
<style>
    .main-title {
        text-align: center;
        color: #164a7f;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .step-badge {
        display: inline-block;
        background-color: #164a7f;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .tip-box {
        background-color: #e8f4f8;
        border-left: 4px solid #2fa6dc;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
"""

# ===== ENVIRONMENT VARIABLES =====
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
APP_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")  # For facilitator dashboard
DATA_PATH = os.getenv("DATA_PATH", "./data")
SAMPLE_DATA_PATH = os.path.join(DATA_PATH, "sample_data")
PROGRAM_CARDS_PATH = os.path.join(DATA_PATH, "program_cards")

# ===== GUIDANCE TEXT =====
PARTICIPANT_GUIDANCE = [
    "Move in order but keep the pace brisk. Aim to make decisions, not perfect prose.",
    "Write directly in the boxes.",
]

SPRINT_CHECKLIST = [
    "Primary outcome and indicator locked in",
    "Randomization unit clear and feasible",
    "Measurement instruments matched to outcomes",
    "Assumptions flagged with validation ideas",
    "Decision trigger recorded and owner assigned",
]

# ===== COACHING PROMPTS (for facilitators) =====
COACHING_PROMPTS = [
    "Where could spillovers or compliance issues weaken this randomization?",
    "Which assumption, if wrong, breaks the theory of change?",
    "How will you measure the primary outcome without overloading the team?",
    "What decision will you make once the first results arrive?",
]
