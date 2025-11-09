# RCT Design Activity: Interactive Workshop App

A comprehensive, interactive application for teaching Randomized Controlled Trial (RCT) design during training workshops. Participants work through a structured design sprint, learning to frame challenges, map theories of change, plan measurement, and randomize treatment assignment—all while designing a real evaluation for their program.

## Overview

This app is an interactive RCT design workbook for workshop participants. Features include:

- **Guided Design Sprint**: Step-by-step workflow mirroring the 6-step participant workbook
- **Program Cards**: Context-specific scenarios (Education, Health, Agriculture) that anchor team discussions
- **Sample Data Generation**: Realistic datasets for each program card to enable practice randomization
- **Randomization Integration**: Embedded link to the [`rct_field_flow`](https://github.com/ajolex/rct_field_flow) app for live randomization
- **Report Export**: Generate professional HTML or PDF reports of the design plan with all participant responses
- **Facilitator Dashboard**: Optional overview for trainers to monitor progress across teams
- **Responsive Design**: Works on laptops, tablets, and mobile devices during in-person workshops

## Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/ajolex/rct-design-activity.git
cd rct-design-activity

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Run the main app
streamlit run app/main.py

# Or run with Streamlit config
streamlit run app/main.py --logger.level=info
```

The app will open at `http://localhost:8501`.

## Folder Structure

```
rct-design-activity/
├── .github/
│   └── workflows/              # CI/CD and deployment automation
│       ├── tests.yml           # Run tests on each push
│       └── deploy.yml          # Auto-deploy to cloud
│
├── app/
│   ├── main.py                 # Entry point and intro page
│   ├── config.py               # App configuration and constants
│   ├── pages/                  # Multi-page app sections
│   │   ├── 1_Program_Cards.py      # Step 0: Select & read program card
│   │   ├── 2_Step_1_Frame_Challenge.py
│   │   ├── 3_Step_2_Theory_of_Change.py
│   │   ├── 4_Step_3_Measurement.py
│   │   ├── 5_Step_4_Randomization.py
│   │   ├── 6_Step_5_Implementation.py
│   │   ├── 7_Step_6_Decision.py
│   │   ├── 8_Generate_Report.py    # Export design plan as HTML/PDF
│   │   └── 9_Admin_Dashboard.py    # Optional facilitator view (password protected)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py        # Workbook steps, guidance, tips
│   │   ├── data_models.py      # Pydantic models for form state
│   │   ├── program_cards.py    # Program card definitions and loaders
│   │   ├── sample_data_gen.py  # Generate realistic datasets
│   │   ├── report_builder.py   # HTML/PDF report generation
│   │   └── validators.py       # Input validation and checks
│   │
│   └── assets/
│       ├── styles/
│       │   ├── main.css        # Custom Streamlit theming
│       │   └── report.css      # Report styling
│       ├── logo.png
│       ├── cover_image.png     # Title slide background
│       └── icons/              # Step icons and graphics
│
├── data/
│   ├── sample_data/
│   │   ├── education_bridge_to_basics.csv
│   │   ├── health_community_care_loop.csv
│   │   └── agriculture_smart_water_boost.csv
│   │
│   └── program_cards/
│       ├── education.json      # Card metadata and descriptions
│       ├── health.json
│       └── agriculture.json
│
├── tests/
│   ├── __init__.py
│   ├── test_sample_data_gen.py
│   ├── test_report_builder.py
│   ├── test_data_models.py
│   └── test_integration.py
│
├── docs/
│   ├── README.md               # This file
│   ├── DEPLOYMENT.md           # Cloud deployment guides
│   ├── API_REFERENCE.md        # Utility function documentation
│   ├── guides/
│   │   ├── FACILITATION.md     # How to run a workshop
│   │   ├── CUSTOMIZATION.md    # Guidance for adapting the app to different contexts
│   │   └── TROUBLESHOOTING.md  # Common issues
│   └── architecture.md         # Technical design overview
│
├── scripts/
│   ├── generate_sample_data.py # Standalone data generator
│   ├── validate_program_cards.py # Check card definitions
│   └── export_template.py      # Export blank template for teams
│
├── .gitignore
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup (optional)
├── streamlit_config.toml       # Streamlit configuration
├── Dockerfile                  # Container setup for deployment
└── docker-compose.yml          # Multi-container orchestration
```

## Core Features

### 1. **Program Card Selection & Display** (`pages/1_Program_Cards.py`)

Participants select their assigned program card and review the context, concept, and decision horizon. Cards are displayed in an engaging, readable format with:

- Context snapshot (problem statement, resources, timeline)
- Program concept (activities, outputs, mechanisms)
- Decision horizon (scale/redesign trigger)
- Reach and budget metrics

### 2. **Design Sprint Pages** (`pages/2-7_Step_*.py`)

Each of the 6 workbook steps is implemented as a Streamlit page with:

- Clear goal and actions
- Guided note-taking sections
- Inline tips and validation
- Progress tracking across the sprint
- Save/restore from session state

### 3. **Sample Data Generation** (`utils/sample_data_gen.py`)

For each program card, generates realistic, randomizable datasets:

- **Education**: School, classroom, student roster with baseline reading scores
- **Health**: Community, mother profiles, baseline health indicators
- **Agriculture**: Farm unit, farmer profiles, baseline soil/water metrics

Data includes:

- Stratification variables (geography, prior performance)
- Baseline outcome measures
- Treatment feasibility flags
- Metadata for randomization (cluster IDs, individual IDs)

### 4. **Randomization Integration** (`pages/5_Step_4_Randomization.py`)

- Link to live [`rct_field_flow`](https://github.com/ajolex/rct_field_flow) randomization app
- Option to upload sample data directly to the randomizer
- Download randomization results
- Display randomization method and assumptions used

### 5. **Report Generation** (`pages/8_Generate_Report.py` + `utils/report_builder.py`)

Exports a professional design report containing:

- Team name and program card
- Responses to all 6 steps
- Theory of change diagram (text-based or embedded)
- Measurement plan summary
- Randomization design and checks
- Implementation timeline
- Decision trigger and next steps
- Available formats: HTML (interactive), PDF (printable), DOCX (editable)

### 6. **Admin Dashboard** (`pages/9_Admin_Dashboard.py`) [Optional]

Facilitator-only view (password protected) showing:

- Teams and their progress
- Current step distribution
- Time elapsed per team
- Quick links to generated reports
- Export all team submissions as Excel

## Session Flow for a 30-Minute Workshop

```
4 min  → Welcome Spark (overview outside app, then launch)
18 min → Design Sprint (pages 1-8 in sequence)
5 min  → Gallery Feedback (teams pull up reports on wall displays)
3 min  → Commit to Next Step (capture decision trigger, assign owner)
```

## Data Models

All form inputs are validated using Pydantic models in `utils/data_models.py`:

```python
class FrameChallenge(BaseModel):
    program_title: str
    target_group: str
    delivery_setting: str
    success_statement: str

class TheoryOfChange(BaseModel):
    riskiest_assumption: str
    early_signal: str

class Measurement(BaseModel):
    primary_outcome: str
    instruments: str
    # ... etc

class DesignPlan(BaseModel):
    team_name: str
    program_card: str
    frame_challenge: FrameChallenge
    theory_of_change: TheoryOfChange
    # ... full design captured
```

## Extending & Customizing

### Add a New Program Card

1. Create a JSON file in `data/program_cards/<new_card>.json`
2. Generate sample data in `data/sample_data/<new_card>.csv`
3. Add entry to `utils/program_cards.py`
4. Test with `scripts/validate_program_cards.py`

### Modify Workbook Steps

Edit the step definitions in `utils/constants.py` (imported from the original workbook).

### Change Report Template

Edit `utils/report_builder.py` and adjust CSS in `app/assets/styles/report.css`.

### Deploy to Cloud

See `docs/DEPLOYMENT.md` for:

- Streamlit Cloud (free tier)
- AWS / Azure / GCP
- Docker + Kubernetes

## Dependencies

See `requirements.txt` for full list. Key packages:

- `streamlit` – UI framework
- `pandas` – Data handling
- `pydantic` – Data validation
- `jinja2` – Report templating
- `weasyprint` or `pdfkit` – PDF export
- `python-docx` – DOCX export

## Testing

Run the test suite:

```bash
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

Tests cover:

- Data model validation
- Sample data generation correctness
- Report generation
- Page navigation and state management
- API integrations

## Deployment

### Local Development

```bash
streamlit run app/main.py --logger.level=debug
```

### Streamlit Cloud

```bash
# Push to GitHub, connect repo to Streamlit Cloud
# App auto-deploys on each push
```

### Docker

```bash
docker build -t rct-design-activity .
docker run -p 8501:8501 rct-design-activity
```

See `docs/DEPLOYMENT.md` for detailed cloud setup.

## Randomization Integration

The app links to the [`rct_field_flow`](https://github.com/ajolex/rct_field_flow) app for randomization:

1. Participant completes Step 4 (Randomization Plan)
2. Clicks "Open Randomizer" button
3. Sample data is formatted and uploaded to `rct_field_flow`
4. Randomizer shows live randomization results
5. Participant downloads results and embeds in report

Alternatively, randomization can be done offline with scripts in `scripts/`.

## Workshop Facilitation

For guidance on running a workshop with this app, see:

- `docs/guides/FACILITATION.md` – Full script and timing
- `docs/guides/CUSTOMIZATION.md` – Guidance for adapting the app to different contexts
- The original `create_rct_booklet.py` – Facilitator prep materials

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

## Support & Feedback

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/ajolex/rct-design-activity/issues)
- **Discussions**: Share ideas in [GitHub Discussions](https://github.com/ajolex/rct-design-activity/discussions)
- **Email**: contact@example.com

## Acknowledgments

- Based on the RCT design workbook and facilitation guide in `create_rct_booklet.py`
- Program cards adapted from real-world education, health, and agriculture contexts
- Randomization functionality via the [`rct_field_flow`](https://github.com/ajolex/rct_field_flow) toolkit

---

**Made with ❤️ for impact-driven practitioners designing rigorous evaluations.**
