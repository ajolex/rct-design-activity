"""
Report generation page - Export final RCT design activity report as HTML or PDF.
Combines all participant responses and design decisions.
"""

import streamlit as st
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Report | RCT Design Activity",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False


def generate_html_report(design_data: dict, randomization_data=None) -> str:
    """Generate comprehensive HTML report of RCT design activity."""
    
    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RCT Design Activity Report</title>
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
                <p class="timestamp">Generated: {timestamp}</p>
            </div>
            
            <!-- Executive Summary -->
            <div class="section">
                <h2>📋 Executive Summary</h2>
                <p>
                    This report documents the completion of the RCT Design Activity, an interactive workshop
                    exercise designed to build practical skills in designing randomized controlled trials (RCTs).
                    Participants progressed through the activity by:
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
            
            <!-- Key Takeaways -->
            <div class="section">
                <h2>✅ Key Takeaways</h2>
                <div class="success-box">
                    <h3>Design Principles Applied:</h3>
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
                <p>For more information, visit: <a href="https://github.com">RCT Design Activity Repository</a></p>
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


def main():
    """Main report generation page."""
    st.title("📄 Generate Final Report")
    
    st.markdown("""
    ### Complete Your RCT Design Activity
    
    You've worked through the complete RCT design process:
    1. ✅ Selected a program
    2. ✅ Designed your RCT
    3. ✅ Generated sample data
    4. ✅ Implemented randomization
    
    Now let's generate your final design report!
    """)
    
    # Report options
    display_report_options()
    
    st.markdown("---")
    st.markdown("### 📝 Generate Your Report")
    
    # Get design data from session state or use sample
    if "design_data" in st.session_state:
        design_data = st.session_state.design_data
    else:
        design_data = generate_sample_report_data()
    
    # Get randomization data if available
    randomization_data = st.session_state.get("randomization_data", None)
    
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
            # Generate HTML report
            html_report = generate_html_report(design_data, randomization_data)
            
            # Display in browser
            st.success("✅ Report generated successfully!")
            st.markdown("---")
            
            # Download button
            st.download_button(
                label="📥 Download HTML Report",
                data=html_report,
                file_name=f"RCT_Design_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            # Preview
            with st.expander("👁️ Preview Report", expanded=True):
                st.markdown(html_report, unsafe_allow_html=True)
        
        elif export_format == "CSV":
            # Create CSV report
            df_report = pd.DataFrame({
                "Category": ["Program", "Research Question", "Primary Outcome", "Sample Size"],
                "Value": [
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
                file_name=f"RCT_Design_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
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
