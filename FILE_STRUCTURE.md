# RCT Design Activity - File Structure & Integration Guide

## 📁 Complete Project Structure

```
rct-design-activity/
├── 📄 README.md                          # Project overview & setup
├── 📄 INTEGRATION_COMPLETE.md            # ✨ Integration status & summary
├── 📋 requirements.txt                   # Python dependencies
├── 🔧 .streamlit/                        # Streamlit configuration
│   └── config.toml
│
├── 📂 app/                               # Main application
│   ├── 📄 main.py                        # Home page & navigation (UPDATED)
│   ├── 🔧 config.py                      # App configuration & styling
│   │
│   ├── 📂 pages/                         # Multi-page app
│   │   ├── introduction.py               # Welcome & orientation
│   │   ├── program_selection.py          # Program card selector
│   │   ├── design_workbook.py            # 6-step design sprint
│   │   ├── 🎲 randomization.py           # ✨ NEW: RCT Field Flow interface
│   │   └── 📄 report_generation.py       # ✨ NEW: Report generation
│   │
│   ├── 📂 assets/                        # Static assets
│   │   └── styles/                       # CSS & styling
│   │
│   └── 📂 utils/                         # Utility modules
│       ├── data_models.py                # Data structures & classes
│       ├── program_cards.py              # Program card data & utilities
│       ├── sample_data_gen.py            # Sample data generation
│       └── helpers.py                    # Helper functions
│
├── 📂 data/                              # Data storage
│   ├── program_cards/                    # Program card definitions
│   └── sample_data/                      # Generated sample datasets
│
├── 📂 docs/                              # Documentation
│   ├── 📄 ARCHITECTURE.md                # System architecture
│   ├── 📄 DEPLOYMENT.md                  # Deployment guide
│   ├── 🎲 RANDOMIZATION_INTEGRATION.md   # ✨ NEW: Integration details
│   ├── 📊 INTEGRATION_SUMMARY.md         # ✨ NEW: Overview & features
│   ├── ⚡ QUICK_REFERENCE.md            # ✨ NEW: Quick lookup
│   └── 📂 guides/                        # Additional guides
│       └── facilitation_guide.md         # Workshop facilitation
│
├── 📂 scripts/                           # Utility scripts
│   └── generate_sample_data.py           # Data generation script
│
└── 📂 tests/                             # Unit tests
    └── test_integration.py               # Integration tests

```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     RCT DESIGN ACTIVITY                         │
└─────────────────────────────────────────────────────────────────┘

1️⃣ START: app/main.py
   ├─ Team name input
   ├─ Program card selection
   └─ Navigation sidebar

2️⃣ DESIGN: pages/program_selection.py + pages/design_workbook.py
   ├─ Review program context
   ├─ Work through 6 design steps
   ├─ Capture RCT design decisions
   ├─ Identify research question, outcomes, confounders
   └─ Plan randomization approach
   
   📊 Data Storage: st.session_state.design_data

3️⃣ DATA: Sample data generation (in design_workbook.py)
   ├─ Create participant roster
   ├─ Define baseline covariates
   ├─ Generate realistic characteristics
   └─ Store for randomization
   
   📊 Data Storage: st.session_state.sample_data

4️⃣ 🎲 RANDOMIZATION: pages/randomization.py
   │
   ├─ Display instructions
   │
   ├─ Embedded iframe (RCT Field Flow)
   │  └─ https://aj-rctfieldflow.streamlit.app/
   │     ├─ Select randomization method
   │     ├─ Configure parameters
   │     ├─ Run randomization
   │     └─ Download results CSV
   │
   ├─ Upload CSV results
   │  ├─ Validate format
   │  ├─ Parse treatment column
   │  ├─ Display distribution
   │  └─ Show balance summary
   │
   └─ Store in session state
      └─ st.session_state.randomization_data
         └─ st.session_state.randomization_exported = True

5️⃣ 📄 REPORT: pages/report_generation.py
   ├─ Retrieve design_data from session
   ├─ Retrieve randomization_data from session
   ├─ Generate HTML report
   │  ├─ Executive summary
   │  ├─ Program information
   │  ├─ Design decisions
   │  ├─ Sample characteristics
   │  ├─ Randomization results
   │  └─ Key takeaways
   ├─ Provide download options
   │  ├─ 📄 HTML (print-friendly)
   │  └─ 📊 CSV (data summary)
   └─ Export & share

END: ✅ Complete workshop with final report
```

## 🔌 Integration Points

### 1. Embedded RCT Field Flow (Main Integration)

**File:** `app/pages/randomization.py`

```python
# Embedded iframe (lines 95-103)
st.markdown("""
    <iframe 
        src="https://aj-rctfieldflow.streamlit.app/?embed=true"
        height="900"
        width="100%"
        frameborder="0"
    ></iframe>
""", unsafe_allow_html=True)

# CSV upload (lines 120-160)
uploaded_file = st.file_uploader(
    "Upload randomized dataset (CSV)",
    type=["csv"]
)
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.randomization_data = df
    st.session_state.randomization_exported = True
```

### 2. Session State for Data Exchange

**File:** `app/config.py`

```python
DEFAULT_SESSION_STATE = {
    "randomization_data": None,           # Randomized dataset
    "randomization_exported": False,      # Export flag
    "design_data": {},                    # Design decisions
    "sample_data": None,                  # Generated sample
    # ... other keys
}
```

### 3. Navigation Links

**File:** `app/main.py`

```python
# Sidebar quick links (lines 55-60)
if st.button("🎲 Randomize"):
    st.switch_page("pages/randomization.py")

if st.button("📊 Generate Report"):
    st.switch_page("pages/report_generation.py")
```

### 4. Report Integration

**File:** `app/pages/report_generation.py`

```python
# Access randomization data (line 290)
randomization_data = st.session_state.get("randomization_data", None)

# Include in report (line 318)
html_report = generate_html_report(design_data, randomization_data)

# Generate treatment distribution (lines 385-400)
if randomization_data is not None:
    treatment_col = next((col for col in randomization_data.columns 
                         if 'treatment' in col.lower()), None)
    if treatment_col:
        dist = randomization_data[treatment_col].value_counts()
```

---

## 📊 Session State Flow

```
┌────────────────────────────────────────────────────────────────┐
│              Streamlit Session State Management                 │
└────────────────────────────────────────────────────────────────┘

config.py:
  DEFAULT_SESSION_STATE initialized
       ↓
main.py:
  for key in DEFAULT_SESSION_STATE:
      st.session_state[key] = value
       ↓
design_workbook.py:
  st.session_state.design_data = {
      "program_name": "...",
      "research_question": "...",
      "sample_size": 300,
      ...
  }
  st.session_state.sample_data = DataFrame
       ↓
randomization.py:
  # After CSV upload
  st.session_state.randomization_data = pd.read_csv(file)
  st.session_state.randomization_exported = True
       ↓
report_generation.py:
  design_data = st.session_state.design_data
  randomization_data = st.session_state.randomization_data
  
  # Generate report with both
  html_report = generate_html_report(
      design_data, 
      randomization_data
  )
```

---

## 🎯 Use Cases

### Use Case 1: Standard Workshop Flow
```
Participant arrives
  → Enter team name
  → Select program card
  → Review program
  → Work through design steps
  → Generate sample data
  → Use RCT Field Flow randomization
  → Upload results
  → Generate & download report
```

### Use Case 2: Facilitator Quick Check
```
Facilitator opens app
  → Switch to specific program
  → Jump to randomization page
  → Check participant CSV
  → Verify treatment distribution
  → Proceed to report
```

### Use Case 3: Post-Workshop Analysis
```
Workshop complete
  → Collect all generated reports
  → Review design decisions across teams
  → Analyze randomization approaches
  → Share examples for next cohort
```

---

## 🛠️ Customization Points

### 1. Add New Program Card
**File:** `app/utils/program_cards.py`
```python
PROGRAM_CARDS = {
    "new_program": {
        "title": "New Program Name",
        "sector": "Sector",
        # ... full program definition
    }
}
```

### 2. Modify Report Template
**File:** `app/pages/report_generation.py`
```python
def _generate_program_section(design_data: dict) -> str:
    # Customize this function
```

### 3. Change Randomization Tool
**File:** `app/pages/randomization.py`
```python
# Change embedded URL if needed
src="https://example-randomization-tool.com/"
```

### 4. Add Database Integration
**File:** `app/config.py`
```python
# Add database configuration
DATABASE_URL = "postgresql://..."
```

---

## 📈 Deployment Checklist

- [ ] Test app locally: `streamlit run app/main.py`
- [ ] Verify embedded iframe loads
- [ ] Test CSV upload/export cycle
- [ ] Generate sample report
- [ ] Deploy to Streamlit Cloud
- [ ] Set environment variables
- [ ] Test production deployment
- [ ] Share with workshop facilitators
- [ ] Collect user feedback
- [ ] Iterate based on feedback

---

## 🔍 Key Metrics to Track

**Completion Metrics:**
- Participants completing all steps
- Randomization success rate
- Report generation success rate

**Quality Metrics:**
- RCT design completeness
- Treatment balance achieved
- Time per step

**Engagement Metrics:**
- Time spent in each section
- Resource access (docs, links)
- Help/support requests

---

## 📞 Getting Help

**Documentation:**
1. `INTEGRATION_COMPLETE.md` - Status & overview
2. `QUICK_REFERENCE.md` - Fast answers
3. `RANDOMIZATION_INTEGRATION.md` - Detailed technical guide
4. `ARCHITECTURE.md` - System design

**Code:**
- Comments throughout code
- Docstrings in functions
- Type hints in functions

**External:**
- RCT Field Flow docs: https://github.com/ajolex/rct_field_flow
- Streamlit docs: https://docs.streamlit.io/

---

## ✅ Integration Status

| Component | Status | File(s) |
|-----------|--------|---------|
| Randomization Interface | ✅ Complete | `pages/randomization.py` |
| Report Generation | ✅ Complete | `pages/report_generation.py` |
| Navigation | ✅ Complete | `main.py` |
| Session State | ✅ Complete | `config.py` |
| Documentation | ✅ Complete | `docs/` |
| Testing | 🟡 Recommended | `tests/` |
| Deployment | 🟡 Ready | `DEPLOYMENT.md` |

---

**Ready to deploy!** 🚀

Start with:
```bash
streamlit run app/main.py
```

---

Last Updated: November 10, 2025
