# Quick Reference: RCT Design Activity + RCT Field Flow Integration

## 🎯 Integration Strategy

**Approach:** Embedded iframe with CSV data exchange  
**URL:** https://aj-rctfieldflow.streamlit.app/  
**Status:** ✅ Ready for use

## 📊 Flow Chart

```
START: app/main.py
  │
  ├─ [DESIGN] Pages 1-6 → Design RCT
  │                          │
  │                          └─> pages/program_selection.py
  │                          └─> pages/design_workbook.py (main steps)
  │
  ├─ [DATA] Sample generation
  │                          │
  │                          └─> Generate participant roster
  │                          └─> Store characteristics
  │
  ├─ [RANDOMIZE] pages/randomization.py ←─── 🎲 RCT Field Flow (embedded)
  │                                              │
  │                                              ├─ Configure method
  │                                              ├─ Set parameters
  │                                              └─ Download CSV
  │
  ├─ [EXPORT] Upload CSV to app
  │                     │
  │                     ├─ Parse CSV
  │                     ├─ Validate treatment column
  │                     └─ Store in session_state.randomization_data
  │
  └─ [REPORT] pages/report_generation.py
                  │
                  ├─ Compile design decisions
                  ├─ Include randomization results
                  ├─ Generate HTML
                  └─ Download report
```

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `app/pages/randomization.py` | Interface for embedded RCT Field Flow tool |
| `app/pages/report_generation.py` | Final report generation (HTML/CSV) |
| `app/main.py` | Updated with navigation links |
| `docs/RANDOMIZATION_INTEGRATION.md` | Detailed integration guide |
| `docs/INTEGRATION_SUMMARY.md` | Overview and quick start |

## 💾 Data Exchange

### CSV Format (Expected from RCT Field Flow)

```
participant_id,age,region,gender,treatment
001,35,North,M,control
002,42,South,F,treatment
003,28,North,M,treatment
```

### Session State

```python
# After CSV upload:
st.session_state.randomization_data      # DataFrame
st.session_state.randomization_exported  # Boolean
```

## 🎲 Using the Embedded Randomizer

### In Browser
1. Participants see embedded iframe
2. Use RCT Field Flow's full interface
3. Configure randomization parameters
4. Download results as CSV

### Alternative (if iframe doesn't work)
- Click link to open in new tab
- https://aj-rctfieldflow.streamlit.app/

## 📥 Uploading Results

### Process
1. Export CSV from RCT Field Flow
2. Upload in "Export Randomization Results" section
3. App validates treatment column exists
4. Displays treatment distribution
5. Stores in session state for report

### Expected Columns
- ✅ ID column (participant_id, caseid, id, etc.)
- ✅ Treatment column (treatment, treatment_arm, arm, etc.)
- ✅ Optional: covariates, strata

## 📄 Report Generation

### HTML Report Includes
- Program information
- Design decisions summary
- Sample characteristics
- Randomization results
- Treatment distribution table
- Key takeaways

### Export Options
- 📄 HTML (print-friendly)
- 📊 CSV (data summary)

## 🚀 Testing Checklist

- [ ] Embedded iframe loads
- [ ] Click "Open RCT Field Flow" link works
- [ ] CSV upload accepts valid file
- [ ] Treatment distribution displays
- [ ] HTML report generates
- [ ] PDF export works (if enabled)
- [ ] Session data persists across pages
- [ ] Back/forward navigation works

## ⚙️ Configuration

### Session State Initialization (in `config.py`)
```python
DEFAULT_SESSION_STATE = {
    "randomization_data": None,
    "randomization_exported": False,
    "design_data": {},
    # ... other keys
}
```

### Randomization Page (in `pages/randomization.py`)
- Embedded URL: `https://aj-rctfieldflow.streamlit.app/?embed=true`
- CSV uploader: `st.file_uploader("Upload randomized dataset (CSV)")`
- Data storage: `st.session_state.randomization_data = df`

## 🔗 Navigation Commands

```python
# From app/main.py to randomization
if st.button("🎲 Randomize"):
    st.switch_page("pages/randomization.py")

# From randomization to report
if st.button("Continue to Report"):
    st.switch_page("pages/report_generation.py")

# From report back to home
if st.button("Return to Home"):
    st.switch_page("app/main.py")
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Embedded app blank | Use alternative link to open in new tab |
| CSV won't upload | Check format, ensure "treatment" column exists |
| Treatment not showing | Column name must contain "treatment" (case-insensitive) |
| Data lost between pages | Check session state initialization |
| Button navigation fails | Verify `st.switch_page()` paths are correct |

## 📚 Related Documentation

- **Detailed Guide:** `docs/RANDOMIZATION_INTEGRATION.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **Setup:** `docs/DEPLOYMENT.md`
- **RCT Field Flow Repo:** https://github.com/ajolex/rct_field_flow
- **Randomization Docs:** https://github.com/ajolex/rct_field_flow/blob/master/docs/RANDOMIZATION.md

## ✨ Features Enabled

✅ Embedded randomization tool  
✅ CSV data exchange  
✅ Treatment distribution analysis  
✅ HTML report generation  
✅ Session state persistence  
✅ Page navigation  
✅ Balance check integration  
✅ Download code (from RCT Field Flow)  

## 🎓 Participant Workflow

```
1. Welcome (1 min)
   ↓
2. Program Card Selection (1 min)
   ↓
3. Review Program (2 min)
   ↓
4. Design Sprint 1-6 (18 min)
   ├─ Challenge framing
   ├─ Theory of change
   ├─ Measurement design
   ├─ Randomization planning
   ├─ Implementation safeguards
   └─ Decision triggers
   ↓
5. Generate Sample Data (2 min)
   ↓
6. Randomization (5 min) ← Embedded RCT Field Flow
   ├─ Upload sample data
   ├─ Configure randomization
   ├─ Run randomization
   └─ Export results
   ↓
7. Report Generation (2 min)
   ├─ View compiled design
   ├─ Check randomization results
   └─ Download report
   ↓
DONE: Total ~30 minutes
```

---

**Quick Links:**
- [Live Randomizer](https://aj-rctfieldflow.streamlit.app/)
- [RCT Field Flow GitHub](https://github.com/ajolex/rct_field_flow)
- [Streamlit Docs](https://docs.streamlit.io/)

**Last Updated:** November 10, 2025
