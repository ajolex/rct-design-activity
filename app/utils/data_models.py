"""
Pydantic data models for validating user input throughout the design sprint.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FrameChallenge(BaseModel):
    """Step 1: Frame the Challenge"""
    program_title: str = Field(..., min_length=5, max_length=200)
    target_group: str = Field(..., min_length=5, max_length=500)
    delivery_setting: str = Field(..., min_length=5, max_length=500)
    success_statement: str = Field(..., min_length=10, max_length=1000)


class TheoryOfChange(BaseModel):
    """Step 2: Map the Theory of Change"""
    riskiest_assumption: str = Field(..., min_length=10, max_length=1000)
    early_signal: str = Field(..., min_length=10, max_length=1000)


class Measurement(BaseModel):
    """Step 3: Design Measurement"""
    primary_outcome_definition: str = Field(..., min_length=10, max_length=1000)
    instruments: str = Field(..., min_length=10, max_length=1000)
    baseline_timing: Optional[str] = None
    followup_timing: Optional[str] = None


class Randomization(BaseModel):
    """Step 4: Plan Randomization"""
    randomization_unit: str = Field(..., min_length=3, max_length=200)
    randomization_method: str = Field(..., min_length=10, max_length=500)
    assignment_steps: str = Field(..., min_length=10, max_length=1000)
    spillover_mitigation: str = Field(..., min_length=10, max_length=1000)


class Implementation(BaseModel):
    """Step 5: Safeguard Implementation"""
    team_checkins: str = Field(..., min_length=10, max_length=1000)
    risks_to_watch: str = Field(..., min_length=10, max_length=1000)


class Decision(BaseModel):
    """Step 6: Decide and Commit"""
    decision_trigger: str = Field(..., min_length=10, max_length=1000)
    stakeholders_to_brief: str = Field(..., min_length=10, max_length=1000)
    next_steps: str = Field(..., min_length=10, max_length=1000)


class DesignPlan(BaseModel):
    """Complete RCT Design Plan"""
    team_name: str = Field(..., min_length=3, max_length=100)
    program_card_id: str
    program_card_title: str
    
    frame_challenge: Optional[FrameChallenge] = None
    theory_of_change: Optional[TheoryOfChange] = None
    measurement: Optional[Measurement] = None
    randomization: Optional[Randomization] = None
    implementation: Optional[Implementation] = None
    decision: Optional[Decision] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    # Optional: Track which steps have been completed
    completed_steps: int = 0

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SampleDataConfig(BaseModel):
    """Configuration for generating sample data"""
    program_card_id: str
    num_clusters: int = Field(default=10, ge=2, le=100)
    num_units_per_cluster: int = Field(default=20, ge=5, le=500)
    random_seed: Optional[int] = None


class RandomizationRequest(BaseModel):
    """Request to randomize sample data"""
    design_plan_id: str
    data_file_path: str
    randomization_method: str
    random_seed: Optional[int] = None


class ReportRequest(BaseModel):
    """Request to generate a report"""
    design_plan: DesignPlan
    report_format: str = Field(default="HTML", regex="^(HTML|PDF|DOCX)$")
    include_sample_data: bool = False
    include_randomization: bool = False
