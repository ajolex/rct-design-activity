# Sample Data for RCT Design Activity

This directory contains baseline data for each of the three program cards used in the RCT design workshop. Participants will use these datasets for practicing randomization techniques.

## Datasets

### 1. Education: Bridge to Basics (`education_bridge_to_basics.csv`)

**Program:** Literacy intervention for grade 4 students in Malawi district schools

**Sample Size:** 1,025 students across 8 schools and 40 classrooms

**Variables:**
- `student_id`: Unique student identifier
- `school_id`: School identifier (1-8)
- `school_name`: School name
- `classroom_id`: Classroom identifier
- `grade_level`: Student grade (4)
- `gender`: Student gender (M/F)
- `baseline_reading_score`: Reading assessment score at baseline (0-100)
- `attendance_rate`: Historical attendance rate (0-1)

**Randomization Unit:** Schools (cluster randomization recommended due to potential spillovers)

**Key Considerations:**
- Stratify by school size or baseline reading scores
- 55% of students read below grade level (score < 50)
- Consider classroom-level contamination

---

### 2. Health: Community Care Loop (`health_community_care_loop.csv`)

**Program:** Maternal postpartum care intervention across 15 communities

**Sample Size:** 607 mothers across 15 communities

**Variables:**
- `mother_id`: Unique mother identifier
- `community_id`: Community identifier (1-15)
- `community_name`: Community name
- `age`: Mother's age (18-45)
- `days_since_delivery`: Days since delivery (1-60)
- `baseline_completed_visits`: Whether completed postpartum visit at baseline (0/1)
- `has_phone`: Whether mother has access to phone for SMS (0/1)
- `education_years`: Years of education completed

**Randomization Unit:** Communities (cluster randomization) or individuals

**Key Considerations:**
- Baseline visit completion rate: 68% (target is 83%+)
- Only 65% have phone access for SMS engagement
- Watch for contamination when health workers serve multiple communities

---

### 3. Agriculture: Smart Water Boost (`agriculture_smart_water_boost.csv`)

**Program:** Drip irrigation and smart farming advisory for smallholder farmers

**Sample Size:** 212 farmers across 12 agricultural co-ops

**Variables:**
- `farmer_id`: Unique farmer identifier
- `coop_id`: Co-op identifier (1-12)
- `coop_name`: Co-op name
- `farm_size_acres`: Farm size in acres
- `baseline_irrigation_method`: Current irrigation method (None/Manual/Partial Drip/Drip)
- `baseline_farm_income_usd`: Annual farm income in USD
- `water_source_type`: Type of water source (Well/Borehole/River/Rain)
- `distance_to_market_km`: Distance to nearest market

**Randomization Unit:** Individual farmers or co-ops (cluster)

**Key Considerations:**
- 45% have no irrigation, 30% manual only
- Current drip irrigation adoption: 18% (partial or full)
- Farm sizes range from 0.26 to 2.96 acres
- Co-op membership may influence spillover effects

---

## Usage in RCT Design Activity

1. **Select Your Program Card** - Choose which program you're designing an RCT for

2. **Download Baseline Data** - Get the corresponding CSV file for your program

3. **Explore the Data** - Understand the population characteristics and baseline indicators

4. **Design Randomization** - Decide on:
   - Unit of randomization (individual vs. cluster)
   - Stratification variables (if any)
   - Treatment:Control ratio (typically 50:50)

5. **Implement Randomization** - Use the RCT Field Flow tool with this data

6. **Check Balance** - Verify randomization created balanced treatment and control groups

---

## Data Generation

These datasets were synthetically generated to reflect realistic characteristics of each program context. The data generation script is located at `app/utils/sample_data_gen.py`.

To regenerate the data:
```python
from app.utils.sample_data_gen import generate_all_sample_data
results = generate_all_sample_data()
```

---

## Notes for Facilitators

- All data is **synthetic** and for training purposes only
- Datasets include realistic features like:
  - Clustering effects (schools, communities, co-ops)
  - Baseline imbalances and variation
  - Missing or incomplete irrigation methods (agriculture)
  - Relevant covariates for stratification
  
- Encourage participants to:
  - Examine baseline balance across potential stratification variables
  - Consider spillover and contamination risks
  - Think about power calculations and sample size adequacy
  - Practice balance checks after randomization
