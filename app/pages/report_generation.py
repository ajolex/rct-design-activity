"""
Report generation page - Export final RCT design activity report as HTML or PDF.
Combines all participant responses and design decisions.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
import io
import zipfile

# Configure page
st.set_page_config(
    page_title="Report | RCT Design Activity",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False


def generate_html_report(team_name: str, design_data: dict, randomization_data=None, randomization_files=None) -> str:
    """Generate comprehensive HTML report of RCT design activity for a specific team."""
    
    if randomization_files is None:
        randomization_files = []
    
    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RCT Design Activity Report - {team_name}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: white;
                padding: 0;
            }}
            
            .container {{
                max-width: 960px;
                margin: 0 auto;
                padding: 40px;
                background: white;
            }}
            
            .header {{
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            
            h1 {{
                color: #1f77b4;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .team-info {{
                background: #e8f4f8;
                padding: 15px;
                border-radius: 4px;
                margin: 15px 0;
                border-left: 4px solid #1f77b4;
            }}
            
            .team-info strong {{
                color: #164a7f;
            }}
            
            .timestamp {{
                color: #666;
                font-size: 0.9em;
                font-style: italic;
            }}
            
            h2 {{
                color: #1f77b4;
                font-size: 1.8em;
                margin-top: 30px;
                margin-bottom: 15px;
                border-left: 4px solid #1f77b4;
                padding-left: 15px;
            }}
            
            h3 {{
                color: #2ca02c;
                font-size: 1.3em;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            
            p {{
                margin-bottom: 15px;
                text-align: justify;
            }}
            
            .section {{
                margin-bottom: 30px;
                page-break-inside: avoid;
            }}
            
            .info-box {{
                background: #f0f7ff;
                border-left: 4px solid #1f77b4;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            
            .success-box {{
                background: #f0fff4;
                border-left: 4px solid #2ca02c;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 0.95em;
            }}
            
            table th {{
                background: #1f77b4;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            table td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            
            table tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            
            table tr:hover {{
                background: #f5f5f5;
            }}
            
            .key-finding {{
                background: #fff3cd;
                padding: 15px;
                margin: 15px 0;
                border-left: 4px solid #ff9800;
                border-radius: 4px;
            }}
            
            .design-element {{
                background: #e8f5e9;
                padding: 15px;
                margin: 15px 0;
                border-left: 4px solid #4caf50;
                border-radius: 4px;
            }}
            
            ul, ol {{
                margin-left: 20px;
                margin-bottom: 15px;
            }}
            
            li {{
                margin-bottom: 8px;
            }}
            
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 0.85em;
                text-align: center;
            }}
            
            .page-break {{
                page-break-after: always;
            }}
            
            code {{
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            @media print {{
                body {{
                    padding: 0;
                }}
                .container {{
                    padding: 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <h1>🎲 RCT Design Activity Report</h1>
                <div class="team-info">
                    <strong>Team:</strong> {team_name}<br>
                    <strong>Generated:</strong> {timestamp}
                </div>
            </div>
            
            <!-- Executive Summary -->
            <div class="section">
                <h2>📋 Executive Summary</h2>
                <p>
                    This report documents {team_name}'s completion of the RCT Design Activity, an interactive workshop
                    exercise designed to build practical skills in designing randomized controlled trials (RCTs).
                    The team progressed through the activity by:
                </p>
                <ul>
                    <li>Understanding RCT fundamentals and design principles</li>
                    <li>Selecting and analyzing a program card case study</li>
                    <li>Working through structured RCT design steps</li>
                    <li>Implementing randomization for treatment assignment</li>
                    <li>Generating a comprehensive design report</li>
                </ul>
            </div>
            
            <!-- Program Information -->
            <div class="section">
                <h2>🎯 Program Information</h2>
                {_generate_program_section(design_data)}
            </div>
            
            <!-- Design Decisions -->
            <div class="section">
                <h2>🏗️ RCT Design Decisions</h2>
                {_generate_design_section(design_data)}
            </div>
            
            <!-- Sample Data -->
            <div class="section">
                <h2>📊 Sample Data Generated</h2>
                {_generate_sample_data_section(design_data)}
            </div>
            
            <!-- Randomization Results -->
            {_generate_randomization_section(randomization_data) if randomization_data is not None else ''}
            
            <!-- Randomization Files Summary -->
            {_generate_randomization_files_summary(randomization_files) if randomization_files else ''}
            
            <!-- Key Takeaways -->
            <div class="section">
                <h2>✅ Key Takeaways</h2>
                <div class="success-box">
                    <h3>Design Principles Applied by {team_name}:</h3>
                    <ul>
                        <li>Clear research question and hypotheses</li>
                        <li>Random assignment to minimize bias</li>
                        <li>Defined treatment and control conditions</li>
                        <li>Measurable outcomes and success metrics</li>
                        <li>Power calculations and sample size considerations</li>
                        <li>Plan for handling confounding variables</li>
                    </ul>
                </div>
            </div>
            
            <!-- Resources -->
            <div class="section">
                <h2>📚 Additional Resources</h2>
                <ul>
                    <li><strong>RCT Field Flow:</strong> Comprehensive toolkit for RCT field operations
                        (<a href="https://github.com/ajolex/rct_field_flow">GitHub</a>)</li>
                    <li><strong>Randomization Tool:</strong> Live app at 
                        <a href="https://aj-rctfieldflow.streamlit.app/">RCT Field Flow</a></li>
                    <li><strong>Design Activity App:</strong> Interactive training resource</li>
                </ul>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p>This report was generated by the RCT Design Activity Streamlit App.</p>
                <p>Team: <strong>{team_name}</strong> | Report Date: {timestamp}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


def _generate_program_section(design_data: dict) -> str:
    """Generate program information section."""
    program_name = design_data.get("program_name", "Not specified")
    program_description = design_data.get("program_description", "")
    program_context = design_data.get("program_context", "")
    
    html = f"""
    <div class="design-element">
        <h3>{program_name}</h3>
        <p><strong>Description:</strong> {program_description}</p>
        <p><strong>Context:</strong> {program_context}</p>
    </div>
    """
    return html


def _generate_design_section(design_data: dict) -> str:
    """Generate RCT design decisions section."""
    
    research_question = design_data.get("research_question", "Not specified")
    primary_outcome = design_data.get("primary_outcome", "Not specified")
    secondary_outcomes = design_data.get("secondary_outcomes", [])
    randomization_method = design_data.get("randomization_method", "Simple random assignment")
    sample_size = design_data.get("sample_size", "Not calculated")
    power = design_data.get("power", "Not specified")
    confounders = design_data.get("potential_confounders", [])
    
    outcomes_html = "".join([f"<li>{outcome}</li>" for outcome in secondary_outcomes])
    confounders_html = "".join([f"<li>{confounder}</li>" for confounder in confounders])
    
    html = f"""
    <div class="design-element">
        <h3>Research Question</h3>
        <p>{research_question}</p>
    </div>
    
    <div class="design-element">
        <h3>Primary Outcome</h3>
        <p>{primary_outcome}</p>
    </div>
    
    <div class="design-element">
        <h3>Secondary Outcomes</h3>
        <ul>{outcomes_html or '<li>Not specified</li>'}</ul>
    </div>
    
    <div class="design-element">
        <h3>Randomization Method</h3>
        <p>{randomization_method}</p>
    </div>
    
    <div class="design-element">
        <h3>Sample Size & Power</h3>
        <p><strong>Target Sample Size:</strong> {sample_size}</p>
        <p><strong>Expected Power:</strong> {power}</p>
    </div>
    
    <div class="design-element">
        <h3>Potential Confounders</h3>
        <ul>{confounders_html or '<li>Not specified</li>'}</ul>
    </div>
    """
    
    return html


def _generate_sample_data_section(design_data: dict) -> str:
    """Generate sample data section."""
    
    num_samples = design_data.get("num_samples", 0)
    sample_characteristics = design_data.get("sample_characteristics", {})
    
    html = f"""
    <p>
        A total of <strong>{num_samples} sample records</strong> were generated for the randomization process.
    </p>
    
    <h3>Sample Characteristics</h3>
    <table>
        <tr>
            <th>Characteristic</th>
            <th>Description</th>
        </tr>
    """
    
    for char, value in sample_characteristics.items():
        html += f"<tr><td>{char}</td><td>{value}</td></tr>"
    
    html += """
    </table>
    """
    
    return html


def _generate_randomization_section(randomization_data: pd.DataFrame) -> str:
    """Generate randomization results section."""
    
    html = """
    <div class="section">
        <h2>🎲 Randomization Results</h2>
        <div class="success-box">
    """
    
    # Treatment distribution
    treatment_col = next((col for col in randomization_data.columns if 'treatment' in col.lower()), None)
    
    if treatment_col:
        dist = randomization_data[treatment_col].value_counts()
        html += f"<h3>Treatment Distribution (n={len(randomization_data)})</h3>"
        html += "<table><tr><th>Treatment Group</th><th>Count</th><th>Percentage</th></tr>"
        
        for arm, count in dist.items():
            pct = (count / len(randomization_data)) * 100
            html += f"<tr><td>{arm}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        
        html += "</table>"
    
    html += """
        </div>
    </div>
    """
    
    return html


def _generate_randomization_files_summary(randomization_files) -> str:
    """Generate a summary section for uploaded randomization files with tabulated summaries."""
    if not randomization_files:
        return ""
    
    # Extract summary data
    summary = _extract_randomization_summary(randomization_files)
    
    html = """
    <div class="section">
        <h2>� Randomization Summary</h2>
        <div class="info-box">
            <h3>Uploaded Randomization Files</h3>
            <p>The following randomization result files are included with this report:</p>
            <ul>
    """
    
    for file_name in summary["file_names"]:
        html += f"<li>{file_name}</li>"
    
    html += """
            </ul>
        </div>
    """
    
    # Add treatment distribution table
    if summary["treatment_counts"] is not None:
        html += """
        <h3>Treatment Assignment Distribution</h3>
        <table>
            <tr>
                <th>Treatment Arm</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
        """
        
        total = summary["treatment_counts"].sum()
        for arm, count in summary["treatment_counts"].items():
            pct = (count / total) * 100
            html += f"<tr><td>{arm}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        
        html += """
        </table>
        """
    
    # Add balance table preview
    if summary["balance_table"] is not None:
        html += """
        <h3 style="margin-top: 30px;">Balance Table Summary</h3>
        <p style="font-size: 0.9em; color: #666; margin-bottom: 10px;">First 10 rows of balance statistics</p>
        <table style="font-size: 0.85em;">
            <tr>
        """
        
        # Add column headers
        for col in summary["balance_table"].columns[:8]:  # Limit to 8 columns for readability
            html += f"<th>{col}</th>"
        
        html += """
            </tr>
        """
        
        # Add rows
        for idx, row in summary["balance_table"].head(10).iterrows():
            html += "<tr>"
            for col in summary["balance_table"].columns[:8]:
                val = row[col]
                if isinstance(val, float):
                    val = f"{val:.3f}"
                html += f"<td>{val}</td>"
            html += "</tr>"
        
        if len(summary["balance_table"]) > 10:
            html += f"<tr><td colspan='{min(8, len(summary['balance_table'].columns))}' style='text-align: center; font-style: italic; color: #999;'>... {len(summary['balance_table']) - 10} more rows</td></tr>"
        
        html += """
        </table>
        """
    
    html += """
    </div>
    """
    
    return html


def _extract_randomization_summary(randomization_files) -> dict:
    """Extract treatment distribution and balance table from uploaded files."""
    summary = {
        "treatment_counts": None,
        "balance_table": None,
        "file_names": []
    }
    
    if not randomization_files:
        return summary
    
    for file in randomization_files:
        try:
            file_name_lower = file.name.lower()
            
            # Try to read as CSV or Excel
            if file.type == "text/csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Look for treatment column
            treatment_cols = [col for col in df.columns if 'treat' in col.lower()]
            if treatment_cols and summary["treatment_counts"] is None:
                treatment_col = treatment_cols[0]
                summary["treatment_counts"] = df[treatment_col].value_counts().sort_index()
            
            # Look for balance table (typically has multiple outcome/baseline columns)
            if 'balance' in file_name_lower and summary["balance_table"] is None:
                summary["balance_table"] = df
            
            summary["file_names"].append(file.name)
        except Exception:
            pass  # Skip files that can't be read
    
    return summary


def display_report_options():
    """Display report generation options."""
    st.markdown("### 📋 Report Generation Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Available Export Formats:**
        - 📄 HTML (view in browser, print-friendly)
        - 📋 PDF (requires additional setup)
        - 📊 CSV (data only)
        """)
    
    with col2:
        st.markdown("""
        **Report Includes:**
        - Program selection and context
        - RCT design decisions
        - Sample data specifications
        - Randomization results
        - Key takeaways
        - Resource references
        """)


def generate_sample_report_data() -> dict:
    """Generate sample data for demonstration."""
    return {
        "program_name": "Agricultural Productivity Training Program",
        "program_description": "A farmer training program focused on sustainable agriculture practices.",
        "program_context": "Rural communities in developing regions with limited access to agricultural extension services.",
        "research_question": "Does intensive farmer training increase agricultural productivity and income?",
        "primary_outcome": "Agricultural yield (kg per hectare)",
        "secondary_outcomes": [
            "Farmer income (annual revenue)",
            "Adoption of new practices (%)",
            "Soil health indicators"
        ],
        "randomization_method": "Stratified random assignment by farm size",
        "sample_size": 300,
        "power": "80% power to detect 20% effect size",
        "potential_confounders": [
            "Farm size",
            "Farmer experience",
            "Access to credit",
            "Rainfall patterns",
            "Market access"
        ],
        "num_samples": 300,
        "sample_characteristics": {
            "Farm Size": "Small (1-5 ha): 40%, Medium (5-10 ha): 35%, Large (10+ ha): 25%",
            "Farmer Age": "Mean 45 years (SD 12)",
            "Education": "Primary 30%, Secondary 50%, Tertiary 20%",
            "Crop Type": "Maize 45%, Rice 35%, Other 20%"
        }
    }


def _collect_team_responses() -> dict:
    """Collect team's actual responses from the workbook steps."""
    workbook_responses = st.session_state.get("workbook_responses", {})
    
    # Extract responses from the workbook
    design_data = {
        # Step 1: Frame the Challenge
        "program_name": workbook_responses.get("step1_program_title", "Not specified"),
        "target_group": workbook_responses.get("step1_target_group", "Not specified"),
        "delivery_setting": workbook_responses.get("step1_delivery_setting", "Not specified"),
        "research_question": workbook_responses.get("step1_success_statement", "Not specified"),
        "program_description": f"Target: {workbook_responses.get('step1_target_group', '')} in {workbook_responses.get('step1_delivery_setting', '')}",
        
        # Step 2: Theory of Change
        "riskiest_assumption": workbook_responses.get("step2_riskiest_assumption", "Not specified"),
        "early_signal": workbook_responses.get("step2_early_signal", "Not specified"),
        
        # Step 3: Measurement
        "primary_outcome": workbook_responses.get("step3_primary_outcome_definition", "Not specified"),
        "instruments": workbook_responses.get("step3_instruments", "Not specified"),
        "baseline_timing": workbook_responses.get("step3_baseline_timing", "Not specified"),
        "followup_timing": workbook_responses.get("step3_followup_timing", "Not specified"),
        
        # Step 4: Randomization
        "randomization_method": workbook_responses.get("step4_randomization_method", "Not specified"),
        "randomization_unit": workbook_responses.get("step4_randomization_unit", "Not specified"),
        "assignment_steps": workbook_responses.get("step4_assignment_steps", "Not specified"),
        "spillover_mitigation": workbook_responses.get("step4_spillover_mitigation", "Not specified"),
        
        # Step 5: Implementation
        "team_checkins": workbook_responses.get("step5_team_checkins", "Not specified"),
        "risks_to_watch": workbook_responses.get("step5_risks_to_watch", "Not specified"),
        
        # Step 6: Decision
        "decision_trigger": workbook_responses.get("step6_decision_trigger", "Not specified"),
        "stakeholders_to_brief": workbook_responses.get("step6_stakeholders_to_brief", "Not specified"),
        "next_steps": workbook_responses.get("step6_next_steps", "Not specified"),
        
        # Defaults
        "secondary_outcomes": [],
        "sample_size": "Not calculated",
        "power": "Not specified",
        "potential_confounders": [],
        "num_samples": 0,
        "sample_characteristics": {},
    }
    
    return design_data


def main():
    """Main report generation page."""
    st.title("📄 Generate Final Report")
    
    # Get team name from session state
    team_name = st.session_state.get("team_name", "Team Unknown")
    program_card = st.session_state.get("program_card_selected", "Not selected")
    
    st.markdown(f"""
    ### 🎉 {team_name} - Complete Your RCT Design Activity
    
    **Program Card:** {program_card}
    
    You've worked through the complete RCT design process:
    1. ✅ Selected a program
    2. ✅ Designed your RCT (Step 1-6)
    3. ✅ Generated sample data
    4. ✅ Implemented randomization
    
    Now let's generate your final design report!
    """)
    
    # Report options
    display_report_options()
    
    st.markdown("---")
    
    # Randomization results upload section
    st.markdown("### 📊 Upload Randomization Results (Optional)")
    st.info("""
    📎 Upload files related to your randomization:
    - Treatment assignment file (CSV, Excel)
    - Balance tables (CSV, Excel, PDF)
    - Randomization details/logs
    """)
    
    # Initialize randomization files storage in session state
    if "randomization_files" not in st.session_state:
        st.session_state.randomization_files = []
    
    # File uploader for randomization results
    uploaded_files = st.file_uploader(
        "Choose randomization result files",
        type=["csv", "xlsx", "xls", "pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files: treatment assignments, balance tables, etc."
    )
    
    if uploaded_files:
        # Store uploaded files in session state
        st.session_state.randomization_files = uploaded_files
        
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        
        # Extract and display randomization summary
        summary = _extract_randomization_summary(uploaded_files)
        
        # Display uploaded files
        with st.expander("📂 View Uploaded Files", expanded=False):
            for idx, file in enumerate(uploaded_files, 1):
                st.markdown(f"**{idx}. {file.name}** ({file.size/1024:.1f} KB)")
                
                # Try to display preview for CSV files
                if file.type in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                    try:
                        df = pd.read_csv(file) if file.type == "text/csv" else pd.read_excel(file)
                        st.dataframe(df.head(), use_container_width=True)
                    except Exception:
                        st.caption("(Preview not available for this file)")
                else:
                    st.caption(f"File type: {file.type}")
        
        # Display randomization summary
        if summary["treatment_counts"] is not None:
            st.markdown("**Treatment Assignment Summary:**")
            treatment_df = pd.DataFrame({
                "Treatment Arm": summary["treatment_counts"].index,
                "Count": summary["treatment_counts"].values,
                "Percentage": (summary["treatment_counts"].values / summary["treatment_counts"].sum() * 100).round(1)
            })
            st.dataframe(treatment_df, use_container_width=True, hide_index=True)
        
        if summary["balance_table"] is not None:
            st.markdown("**Balance Table Preview:**")
            balance_preview = summary["balance_table"].head(10)
            st.dataframe(balance_preview, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📝 Generate Your Report")
    
    # Gather team's actual responses from workbook
    design_data = _collect_team_responses()
    
    # Get randomization data if available
    randomization_data = st.session_state.get("randomization_data", None)
    randomization_files = st.session_state.get("randomization_files", [])
    
    # Export format selection
    export_format = st.radio(
        "Select export format:",
        options=["HTML", "CSV"],
        horizontal=True,
        help="Choose your preferred report format"
    )
    
    # Generate report button
    if st.button("📄 Generate Report", use_container_width=True, type="primary"):
        
        if export_format == "HTML":
            # Generate HTML report with team name and randomization files
            html_report = generate_html_report(team_name, design_data, randomization_data, randomization_files)
            
            # Display in browser
            st.success("✅ Report generated successfully!")
            st.markdown("---")
            
            # Create a zip file with report and randomization files
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add HTML report
                zip_file.writestr(
                    f"RCT_Design_Report_{team_name.replace(' ', '_')}.html",
                    html_report
                )
                
                # Add uploaded randomization files
                for file in randomization_files:
                    zip_file.writestr(file.name, file.getbuffer())
            
            zip_buffer.seek(0)
            
            # Download button with team name in filename
            st.download_button(
                label="📥 Download HTML Report + Randomization Files (ZIP)",
                data=zip_buffer.getvalue(),
                file_name=f"RCT_Design_Report_{team_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # Also offer direct HTML download
            st.download_button(
                label="📄 Download HTML Report Only",
                data=html_report,
                file_name=f"RCT_Design_Report_{team_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            # Preview
            with st.expander("👁️ Preview Report", expanded=True):
                st.markdown(html_report, unsafe_allow_html=True)
        
        elif export_format == "CSV":
            # Create CSV report
            df_report = pd.DataFrame({
                "Category": ["Team Name", "Program", "Research Question", "Primary Outcome", "Sample Size"],
                "Value": [
                    team_name,
                    design_data.get("program_name", ""),
                    design_data.get("research_question", ""),
                    design_data.get("primary_outcome", ""),
                    design_data.get("sample_size", "")
                ]
            })
            
            csv = df_report.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name=f"RCT_Design_Report_{team_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.dataframe(df_report, use_container_width=True)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Randomization", use_container_width=True):
            st.switch_page("pages/randomization.py")
    
    with col3:
        if st.button("🏠 Return to Home", use_container_width=True):
            st.switch_page("app/main.py")


if __name__ == "__main__":
    main()
