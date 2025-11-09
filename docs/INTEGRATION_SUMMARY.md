# Integration Summary: RCT Field Flow + RCT Design Activity

## Quick Overview

The project now includes a complete RCT design activity Streamlit app with integrated randomization capabilities. Key elements delivered:

## ✅ Implementation Complete

### 1. **Randomization Page** (`pages/randomization.py`)
   - **Embedded iframe** displays the live RCT Field Flow randomization tool
   - Participants use the full feature set: simple, stratified, cluster randomization
   - Balance checks and rerandomization available
   - Instructions guide participants through the workflow

### 2. **Report Generation Page** (`pages/report_generation.py`)
   - Generates comprehensive HTML reports
   - Includes all design decisions from the workbook
   - Incorporates randomization results and treatment distribution
   - Exportable as HTML (print-friendly) or CSV

### 3. **Session State Management**
   - `randomization_data`: Stores the randomized dataset
   - `design_data`: Stores all RCT design decisions
   - Data persists across page navigation

### 4. **Navigation Integration**
   - Main app updated with "🎲 Randomize" quick link
   - Seamless page switching between design → randomization → report
   - Back buttons for easy navigation

## 📊 How It Works

### Workflow Summary
```
Welcome & Program Selection
         ↓
Design Sprint (6 Steps)
- Challenge Framing
- Theory of Change
- Measurement Design
- Randomization Planning
- Implementation Safeguards
- Decision Triggers
         ↓
Sample Data Generation
- Create participant roster
- Define characteristics
         ↓
[NEW] Randomization Page
- View embedded RCT Field Flow
- Configure randomization method
- Run randomization
- Export results to CSV
- Upload results back to app
         ↓
[NEW] Report Generation
- Compile all design decisions
- Include randomization results
- Export as HTML or CSV
```

## 🎯 Key Features

### Randomization Integration
✅ **Embedded iframe** - No new browser tabs needed  
✅ **Live tool** - Access full RCT Field Flow capabilities  
✅ **CSV export/import** - Easy data exchange  
✅ **Balance checks** - Automatic diagnostics  
✅ **Reproducible** - Download Python/Stata code  

### Report Generation
✅ **Comprehensive HTML** - Professional, printable reports  
✅ **Design summary** - All RCT elements captured  
✅ **Randomization results** - Treatment distribution tables  
✅ **Sample data** - Data generation specifications  
✅ **Easy export** - Download with one click  

## 📁 Files Created/Modified

### New Files
```
app/pages/randomization.py              → Randomization interface
app/pages/report_generation.py          → Report generation module
docs/RANDOMIZATION_INTEGRATION.md       → Integration documentation
```

### Modified Files
```
app/main.py                             → Added randomization & report quick links
```

## 🚀 Quick Start for Testing

### 1. Test the Randomization Page
```bash
# Run the app (from rct-design-activity directory)
streamlit run app/main.py

# Navigate to 🎲 Randomization quick link
# Try the embedded RCT Field Flow tool
```

### 2. Test CSV Upload
- Download sample data from RCT Field Flow
- Upload to the randomization page
- Verify treatment distribution displays correctly

### 3. Test Report Generation
- Complete design workbook
- Generate report as HTML
- Download and view in browser

## 💡 Best Practices for Integration

### 1. **Workflow Design**
The integrated approach maintains participant flow:
- Design first (workbook steps)
- Then randomize (RCT Field Flow)
- Finally report (consolidated summary)

### 2. **Data Exchange**
- Randomization data stored in session state
- No external database needed
- Session-based persistence
- CSV as standard exchange format

### 3. **User Experience**
- Embedded tool reduces context switching
- Clear instructions at each step
- Back/forward navigation intuitive
- Progress tracking maintained

## 🔧 Technical Details

### Session State Keys
```python
# Key storage locations
st.session_state.randomization_data      # DataFrame from uploaded CSV
st.session_state.randomization_exported  # Boolean flag
st.session_state.design_data             # Design decisions dict
```

### Page Navigation
```python
# Switch between pages
st.switch_page("pages/randomization.py")
st.switch_page("pages/report_generation.py")
st.switch_page("app/main.py")
```

### Expected CSV Structure (from RCT Field Flow)
```
participant_id,age,region,gender,treatment
001,35,North,M,control
002,42,South,F,treatment
003,28,North,M,treatment
```

## 🎓 Facilitation Notes

### For Workshop Facilitators

**Before the workshop:**
1. Test the app end-to-end
2. Familiarize with RCT Field Flow tool
3. Prepare sample datasets
4. Test CSV import process

**During the workshop:**
1. Guide participants through design steps
2. Explain randomization importance
3. Have backup randomized datasets ready
4. Be prepared to help with CSV format issues

**After the workshop:**
1. Collect generated reports
2. Use for participant feedback
3. Archive for documentation
4. Share example reports with next cohort

## 📚 Resources

**Documentation:**
- `docs/RANDOMIZATION_INTEGRATION.md` - Detailed integration guide
- `docs/ARCHITECTURE.md` - App architecture overview
- `docs/DEPLOYMENT.md` - Deployment instructions
- GitHub repo structure in README

**External Tools:**
- [RCT Field Flow](https://github.com/ajolex/rct_field_flow)
- [Live Randomization Tool](https://aj-rctfieldflow.streamlit.app/)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🐛 Troubleshooting

### Issue: Embedded app doesn't load
**Solution:** Use alternative link to open RCT Field Flow in new tab

### Issue: CSV upload fails
**Solution:** Ensure CSV has "treatment" column and valid formatting

### Issue: Data not persisting between pages
**Solution:** Check session state initialization in config.py

## ✨ Next Steps (Optional Enhancements)

1. **CSV Template Generator**
   - Auto-generate pre-formatted upload templates
   - Reduce data entry errors

2. **PDF Export**
   - Add PDF report option (requires WeasyPrint)
   - Professional printed reports

3. **SurveyCTO Integration**
   - Direct upload to SurveyCTO
   - Real-time monitoring dashboard

4. **Analytics Dashboard**
   - Track design decisions across cohorts
   - Identify common challenges
   - Provide facilitation insights

## 📞 Support

- **Questions about integration?** Check `docs/RANDOMIZATION_INTEGRATION.md`
- **App not working?** Review `docs/TROUBLESHOOTING.md` (if created)
- **Want to modify?** Architecture is in `docs/ARCHITECTURE.md`

---

**Status:** ✅ Complete - Ready for Workshop  
**Last Updated:** November 10, 2025  
**Integration Approach:** Embedded iframe with CSV data exchange
