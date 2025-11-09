# Project Structure Documentation

## Overview

The RCT Design Activity app is organized into a modular structure that separates concerns, making it easy to maintain, test, and extend.

## Directory Tree

```
rct-design-activity/
├── .github/
│   └── workflows/                    # CI/CD automation
│       ├── tests.yml                 # Run pytest on push
│       └── deploy.yml                # Deploy to Streamlit Cloud
│
├── app/                              # Main application code
│   ├── __init__.py
│   ├── main.py                       # Streamlit entry point (home page)
│   ├── config.py                     # Configuration & constants
│   │
│   ├── pages/                        # Streamlit multi-page navigation
│   │   ├── 1_Program_Cards.py        # Display & interact with cards
│   │   ├── 2_Step_1_Frame_Challenge.py
│   │   ├── 3_Step_2_Theory_of_Change.py
│   │   ├── 4_Step_3_Measurement.py
│   │   ├── 5_Step_4_Randomization.py
│   │   ├── 6_Step_5_Implementation.py
│   │   ├── 7_Step_6_Decision.py
│   │   ├── 8_Generate_Report.py      # Export design plan
│   │   └── 9_Admin_Dashboard.py      # Facilitator view (optional)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py              # Shared constants from workbook
│   │   ├── data_models.py            # Pydantic validation models
│   │   ├── program_cards.py          # Card loading & management
│   │   ├── sample_data_gen.py        # Generate realistic datasets
│   │   ├── report_builder.py         # HTML/PDF/DOCX export
│   │   └── validators.py             # Custom validation logic
│   │
│   └── assets/
│       ├── styles/
│       │   ├── main.css              # Streamlit theme overrides
│       │   └── report.css            # Report export styling
│       ├── logo.png
│       ├── cover_image.png
│       └── icons/
│           ├── step1.svg
│           ├── step2.svg
│           ├── ... etc
│
├── data/
│   ├── sample_data/                  # Generated CSV files
│   │   ├── education_bridge_to_basics.csv
│   │   ├── health_community_care_loop.csv
│   │   └── agriculture_smart_water_boost.csv
│   │
│   └── program_cards/                # Card definitions (JSON)
│       ├── education.json
│       ├── health.json
│       └── agriculture.json
│
├── tests/
│   ├── __init__.py
│   ├── test_sample_data_gen.py       # Test data generation
│   ├── test_report_builder.py        # Test report export
│   ├── test_data_models.py           # Test validation
│   ├── test_program_cards.py         # Test card loading
│   └── test_integration.py           # End-to-end tests
│
├── docs/
│   ├── README.md                     # Main documentation
│   ├── DEPLOYMENT.md                 # Cloud setup guides
│   ├── API_REFERENCE.md              # Function documentation
│   ├── ARCHITECTURE.md               # Technical overview
│   └── guides/
│       ├── FACILITATION.md           # How to run workshop
│       ├── CUSTOMIZATION.md          # Adapt for your context
│       └── TROUBLESHOOTING.md        # Common issues & fixes
│
├── scripts/
│   ├── generate_sample_data.py       # Standalone data generation
│   ├── validate_program_cards.py     # Validate card definitions
│   └── export_template.py            # Export blank template
│
├── .gitignore
├── .streamlit/
│   └── config.toml                   # Streamlit configuration
│
├── requirements.txt                   # Python dependencies
├── setup.py                          # Package installation (optional)
├── Dockerfile                        # Container setup
├── docker-compose.yml                # Multi-container orchestration
├── pyproject.toml                    # Python project metadata
└── LICENSE                           # MIT License
```

## Module Descriptions

### `app/main.py`
**Purpose:** Streamlit entry point (home page)
**Key Features:**
- Welcome introduction and guidance
- Team name input (session identifier)
- Program card selection
- Progress tracking
- Sidebar navigation
- Session state initialization

### `app/config.py`
**Purpose:** Centralized configuration and constants
**Contents:**
- App metadata (title, subtitle, description)
- Program card definitions (all 3 cards)
- Workbook steps (6 steps with goals, actions, tips)
- Default session state
- UI styling constants
- Environment variables

### `app/pages/` (Streamlit Pages)
Each step of the design sprint has its own page:

- **1_Program_Cards.py** – Select and display the assigned card
- **2_Step_1_Frame_Challenge.py** – Challenge framing with form inputs
- **3_Step_2_Theory_of_Change.py** – Theory mapping with canvas
- **4_Step_3_Measurement.py** – Measurement planning with tables
- **5_Step_4_Randomization.py** – Randomization design + link to rct_field_flow
- **6_Step_5_Implementation.py** – Implementation safeguards
- **7_Step_6_Decision.py** – Decision triggers and commitments
- **8_Generate_Report.py** – Export design plan as HTML/PDF/DOCX
- **9_Admin_Dashboard.py** – Optional facilitator dashboard (password protected)

### `app/utils/data_models.py`
**Purpose:** Pydantic models for input validation
**Models:**
- `FrameChallenge` – Step 1 inputs
- `TheoryOfChange` – Step 2 inputs
- `Measurement` – Step 3 inputs
- `Randomization` – Step 4 inputs
- `Implementation` – Step 5 inputs
- `Decision` – Step 6 inputs
- `DesignPlan` – Complete plan container
- `SampleDataConfig` – Data generation parameters
- `ReportRequest` – Report export parameters

### `app/utils/program_cards.py`
**Purpose:** Load and manage program cards
**Functions:**
- `get_all_program_cards()` – Returns all 3 cards
- `get_program_card(card_id)` – Fetch by ID
- `get_cards_by_sector(sector)` – Filter by sector
- `format_card_for_display(card)` – UI-ready format
- `load_card_from_json(path)` – Custom card loader
- `save_card_to_json(data, path)` – Save custom cards

### `app/utils/sample_data_gen.py`
**Purpose:** Generate realistic datasets for practice randomization
**Datasets:**
1. **Education** – School clusters with classrooms and students
   - 8 schools, 5 classrooms each, ~600 students total
   - Baseline reading scores, attendance rates
   
2. **Health** – Community clusters with mothers
   - 15 communities, ~600 mothers total
   - Postpartum visit completion, phone access, age
   
3. **Agriculture** – Co-op clusters with farmers
   - 12 co-ops, ~220 farmers total
   - Farm size, irrigation method, baseline income, water source

**Key Functions:**
- `generate_education_data()` – Education dataset
- `generate_health_data()` – Health dataset
- `generate_agriculture_data()` – Agriculture dataset
- `generate_all_sample_data()` – All three datasets
- `save_sample_data()` – Export to CSV
- `load_sample_data()` – Load from CSV

### `app/utils/report_builder.py` (To Be Created)
**Purpose:** Export design plan as HTML, PDF, or DOCX
**Functions:**
- `build_html_report(design_plan)` – HTML export
- `build_pdf_report(design_plan)` – PDF export
- `build_docx_report(design_plan)` – DOCX export
- `render_report_template(design_plan)` – Template rendering

### `tests/` (Unit & Integration Tests)
**Coverage:**
- Data model validation
- Sample data generation correctness
- Report generation format/content
- Program card loading
- Page navigation state management
- API integrations

## Session State Structure

```python
st.session_state = {
    "team_name": "Team Alpha",
    "program_card_selected": "education_bridge_to_basics",
    "current_step": 3,
    "responses": {
        "frame_challenge": {
            "program_title": "...",
            "target_group": "...",
            # ... all Step 1 fields
        },
        "theory_of_change": {
            "riskiest_assumption": "...",
            # ... Step 2 fields
        },
        # ... Steps 3-6
    },
    "sample_data_generated": True,
    "sample_data_file": "education_bridge_to_basics_2024-11-10.csv",
    "report_generated": False,
    "start_time": datetime(2024, 11, 10, 9, 0, 0),
}
```

## Data Flow

```
User Input
    ↓
[Streamlit Page] – captures form data
    ↓
[Pydantic Model] – validates input
    ↓
[Session State] – stores responses
    ↓
[Report Builder] – synthesizes responses into report
    ↓
[Export] – HTML / PDF / DOCX output
```

## Randomization Integration Flow

```
Step 4: Randomization Page
    ↓
[Load Sample Data] – from data/sample_data/
    ↓
[Format for rct_field_flow] – JSON upload format
    ↓
[Link to rct_field_flow] – external randomizer app
    ↓
[Download Results] – randomization assignments
    ↓
[Embed in Report] – include in final export
```

## Adding New Content

### Add a New Program Card
1. Add to `PROGRAM_CARDS` dict in `app/config.py`
2. Generate sample data in `app/utils/sample_data_gen.py`
3. Save CSV to `data/sample_data/`
4. Test with `scripts/validate_program_cards.py`

### Customize Report Template
Edit `app/utils/report_builder.py` and style in `app/assets/styles/report.css`

### Add New Validation Rule
Add Pydantic validator to `app/utils/data_models.py` using `@field_validator` decorator

### Extend Program Card Details
Update `format_card_for_display()` in `app/utils/program_cards.py` to add new sections

## File Naming Conventions

- **Python modules:** `snake_case.py`
- **Streamlit pages:** `N_Page_Title.py` (number for ordering)
- **Data files:** `sector_program_name.csv`
- **Config files:** `config_type.toml` or `config_type.json`
- **Styles:** `component_purpose.css`

## Import Path Examples

```python
# From main app
from app.config import APP_TITLE, WORKBOOK_STEPS
from app.utils.program_cards import get_program_card
from app.utils.sample_data_gen import generate_education_data
from app.utils.data_models import DesignPlan

# From tests
from app.utils.sample_data_gen import generate_education_data
from app.utils.data_models import FrameChallenge
```

---

For deployment and facilitation guides, see `docs/DEPLOYMENT.md` and `docs/guides/FACILITATION.md`.
