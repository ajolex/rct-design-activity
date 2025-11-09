# RCT Field Flow Integration Guide

## Overview

The RCT Design Activity Streamlit app integrates with the **RCT Field Flow** randomization tool to provide participants with a complete RCT design experience. This document outlines the integration strategy, best practices, and technical implementation.

## Integration Approach

### Best Practice: Embedded iframe with Data Exchange

The randomization integration uses an **iframe embedding strategy** with the following advantages:

✅ **Strengths:**
- Maintains workflow continuity - participants stay in the design activity app
- No code refactoring needed - leverages the live RCT Field Flow app
- Participants access the full randomization capabilities
- Results can be easily exported and imported back for reporting
- Transparent - participants see the exact randomization tool being used

### Live Randomization App

**URL:** https://aj-rctfieldflow.streamlit.app/

The embedded randomization tool provides:
- Simple, stratified, cluster, and combined randomization methods
- Automatic balance checks on selected covariates
- Reproducible randomization with seed-based assignment
- Downloadable code (Python and Stata) for transparency
- Optional rerandomization (1-10,000 iterations)

## Workflow Integration

### Participant Journey

```
1. Program Selection
   ↓
2. RCT Design Sprint (6 steps)
   - Challenge framing
   - Theory of change
   - Measurement design
   - Randomization planning
   - Implementation safeguards
   - Decision triggers
   ↓
3. Sample Data Generation
   - Create realistic participant roster
   - Define participant characteristics
   ↓
4. Randomization (Step: pages/randomization.py)
   - Review randomization methods
   - Use embedded RCT Field Flow tool
   - Configure randomization parameters
   - Export randomized dataset
   ↓
5. Report Generation (Step: pages/report_generation.py)
   - Compile design decisions
   - Include randomization results
   - Export as HTML or CSV
```

## Technical Implementation

### File Structure

```
app/pages/
├── randomization.py          # Randomization interface with embedded iframe
└── report_generation.py      # Final report generation

Session State Keys:
├── randomization_data        # Stores the randomized dataset
├── randomization_exported    # Boolean flag for successful export
└── design_data              # Stores all design decisions
```

### Session State Management

The app uses Streamlit session state to persist user data across pages:

```python
# In randomization.py
st.session_state.randomization_data = df  # Store imported data
st.session_state.randomization_exported = True  # Flag for completion

# In report_generation.py
randomization_data = st.session_state.get("randomization_data", None)
# Use in report generation
```

## Using the Embedded Tool

### Step 1: Access the Tool
Participants access the embedded RCT Field Flow interface directly in the Streamlit app (pages/randomization.py).

### Step 2: Configure Randomization
Within the embedded iframe, participants:
1. Select their randomization method
2. Configure treatment arms and proportions
3. Set stratification variables (if needed)
4. Choose a random seed
5. Review balance checks

### Step 3: Export Results
After successful randomization:
1. Download the randomized dataset (CSV) from RCT Field Flow
2. Upload the CSV in the "Export Randomization Results" section
3. Review the treatment distribution and balance summary

### Step 4: Use in Report
The randomization data is automatically included in the final report:
- Treatment distribution table
- Summary statistics by treatment arm
- Balance check results

## Data Exchange Format

### Expected CSV Structure

The randomized dataset exported from RCT Field Flow should include:

```
participant_id, age, region, gender, treatment
001, 35, North, M, control
002, 42, South, F, treatment
003, 28, North, M, treatment
...
```

**Required columns:**
- Participant/case ID column (identified automatically)
- Treatment assignment column (contains arm names)

**Optional columns:**
- Baseline covariates (age, region, gender, etc.)
- Stratification variables
- Contact information

### Report Integration

The report automatically detects:
- Total participant count
- Treatment groups and proportions
- Balance summary by treatment arm
- Number of arms

## Troubleshooting

### Embedded App Not Loading
**Issue:** White screen or "Page not found" in iframe

**Solution:**
1. Check browser console for CORS errors (usually not a problem with Streamlit)
2. Verify internet connection
3. Use the alternative link button to open RCT Field Flow in new tab
4. Alternative URL: https://aj-rctfieldflow.streamlit.app/

### CSV Upload Fails
**Issue:** Error reading uploaded file

**Troubleshooting steps:**
1. Verify file is valid CSV (open in Excel or text editor)
2. Check for special characters in column names
3. Ensure at least one "treatment" column exists
4. Verify column names don't have leading/trailing spaces

### Missing Treatment Distribution
**Issue:** Balance check not showing data

**Solution:**
1. Ensure CSV has a column with "treatment" in the name (case-insensitive)
2. Common names: treatment, treatment_arm, arm, group
3. Check for leading underscores or spaces in column name

## Advanced Customization

### Option 1: Direct Integration (Advanced)
For teams that prefer to avoid the iframe and call RCT Field Flow functions directly:

```python
# Would require importing rct_field_flow as a package
# from rct_field_flow.randomization import RandomizationEngine

# However, this is NOT recommended because:
# - Increases dependency management complexity
# - Requires maintaining compatibility with rct_field_flow updates
# - Embedded iframe is simpler and more maintainable
```

### Option 2: Custom Randomization Interface
Could build a custom randomization interface that:
- Mirrors RCT Field Flow's functionality
- Connects to RCT Field Flow's backend API
- Still allows accessing the full tool

**Recommendation:** Use the embedded iframe approach (current implementation) for simplicity and reliability.

## Security & Privacy Considerations

1. **Data Privacy:** 
   - Uploaded CSV files stay within the Streamlit session
   - No data is sent to external servers
   - Session data cleared when session expires

2. **Reproducibility:**
   - Include random seed in final report
   - Share randomization code downloaded from RCT Field Flow
   - Document all randomization parameters

## Future Enhancements

Potential improvements:

1. **CSV Download Template**
   - Provide pre-formatted CSV template based on sample size
   - Reduce participant data entry errors

2. **Real-time Balance Visualization**
   - Show balance diagnostics immediately after upload
   - Suggest rerandomization if needed

3. **Integration with SurveyCTO**
   - Direct upload of randomized cases to SurveyCTO
   - Automatic case tracking and monitoring

4. **Outcome Tracking**
   - Link randomization to follow-up survey data
   - Calculate treatment effects in real-time

## Resources

- **RCT Field Flow Repository:** https://github.com/ajolex/rct_field_flow
- **Live Randomization Tool:** https://aj-rctfieldflow.streamlit.app/
- **Randomization Documentation:** https://github.com/ajolex/rct_field_flow/docs/RANDOMIZATION.md
- **Streamlit Documentation:** https://docs.streamlit.io/

## Support

For issues or questions about:
- **RCT Field Flow:** See GitHub issues or documentation
- **Design Activity App:** Contact workshop facilitator
- **Streamlit Integration:** See Streamlit documentation

---

**Last Updated:** November 10, 2025
**Status:** Complete integration with embedded RCT Field Flow
