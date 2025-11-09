"""
Generate realistic sample data for each program card.
These datasets can be used for randomization practice during the workshop.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_education_data(
    n_schools: int = 8,
    n_classrooms_per_school: int = 5,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate sample data for Education: Bridge to Basics program.
    
    Includes:
    - School (cluster)
    - Classroom within school
    - Student ID
    - Baseline reading score (0-100)
    - Grade level
    - Gender
    
    Args:
        n_schools: Number of schools (randomization clusters)
        n_classrooms_per_school: Classrooms per school
        random_seed: Seed for reproducibility
    
    Returns:
        DataFrame with student roster and baseline measures
    """
    np.random.seed(random_seed)
    
    rows = []
    student_id = 1000
    
    for school_id in range(1, n_schools + 1):
        school_name = f"School_{school_id:02d}"
        
        for classroom_id in range(1, n_classrooms_per_school + 1):
            classroom_code = f"{school_id:02d}C{classroom_id}"
            
            n_students = np.random.randint(15, 35)  # 15-35 students per classroom
            
            for _ in range(n_students):
                student_id += 1
                
                rows.append({
                    "student_id": student_id,
                    "school_id": school_id,
                    "school_name": school_name,
                    "classroom_id": classroom_code,
                    "grade_level": 4,
                    "gender": np.random.choice(["M", "F"]),
                    "baseline_reading_score": np.random.normal(loc=45, scale=20),  # Mean 45, SD 20
                    "attendance_rate": np.random.uniform(0.6, 0.95),
                })
    
    df = pd.DataFrame(rows)
    df["baseline_reading_score"] = df["baseline_reading_score"].clip(0, 100)
    df = df.round(2)
    
    return df.reset_index(drop=True)


def generate_health_data(
    n_communities: int = 15,
    n_mothers_per_community: int = 40,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate sample data for Health: Community Care Loop program.
    
    Includes:
    - Community (cluster)
    - Mother ID
    - Age
    - Baseline postpartum visit completion (0/1)
    - Days since delivery
    - Has phone (for SMS engagement)
    
    Args:
        n_communities: Number of communities (randomization clusters)
        n_mothers_per_community: Average mothers per community
        random_seed: Seed for reproducibility
    
    Returns:
        DataFrame with mother roster and baseline health indicators
    """
    np.random.seed(random_seed)
    
    rows = []
    mother_id = 5000
    
    for community_id in range(1, n_communities + 1):
        community_name = f"Community_{community_id:02d}"
        n_mothers = np.random.randint(int(n_mothers_per_community * 0.8), n_mothers_per_community + 10)
        
        for _ in range(n_mothers):
            mother_id += 1
            
            rows.append({
                "mother_id": mother_id,
                "community_id": community_id,
                "community_name": community_name,
                "age": np.random.randint(18, 45),
                "days_since_delivery": np.random.randint(1, 60),
                "baseline_completed_visits": np.random.binomial(n=1, p=0.7),  # 70% baseline completion
                "has_phone": np.random.binomial(n=1, p=0.65),  # 65% have phone
                "education_years": np.random.randint(0, 13),
            })
    
    df = pd.DataFrame(rows)
    return df.reset_index(drop=True)


def generate_agriculture_data(
    n_coops: int = 12,
    n_farmers_per_coop: int = 18,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate sample data for Agriculture: Smart Water Boost program.
    
    Includes:
    - Co-op (cluster)
    - Farmer ID
    - Farm size (acres)
    - Baseline irrigation method (traditional/partial/none)
    - Baseline farm income (USD)
    - Water source access
    
    Args:
        n_coops: Number of co-ops (randomization clusters)
        n_farmers_per_coop: Average farmers per co-op
        random_seed: Seed for reproducibility
    
    Returns:
        DataFrame with farmer roster and baseline indicators
    """
    np.random.seed(random_seed)
    
    rows = []
    farmer_id = 3000
    
    for coop_id in range(1, n_coops + 1):
        coop_name = f"Coop_{coop_id:02d}"
        n_farmers = np.random.randint(int(n_farmers_per_coop * 0.75), n_farmers_per_coop + 8)
        
        for _ in range(n_farmers):
            farmer_id += 1
            
            rows.append({
                "farmer_id": farmer_id,
                "coop_id": coop_id,
                "coop_name": coop_name,
                "farm_size_acres": np.random.uniform(0.25, 3),
                "baseline_irrigation_method": np.random.choice(
                    ["None", "Manual", "Partial Drip", "Drip"], p=[0.45, 0.3, 0.2, 0.05]
                ),
                "baseline_farm_income_usd": np.random.gamma(shape=2, scale=200),  # Right-skewed
                "water_source_type": np.random.choice(["Well", "Borehole", "River", "Rain"]),
                "distance_to_market_km": np.random.exponential(scale=5),
            })
    
    df = pd.DataFrame(rows)
    df["farm_size_acres"] = df["farm_size_acres"].round(2)
    df["baseline_farm_income_usd"] = df["baseline_farm_income_usd"].round(2)
    df["distance_to_market_km"] = df["distance_to_market_km"].round(2)
    
    return df.reset_index(drop=True)


def save_sample_data(df: pd.DataFrame, output_path: Path) -> Path:
    """
    Save sample data to a CSV file.
    
    Args:
        df: DataFrame to save
        output_path: Where to save the CSV
    
    Returns:
        Path to the saved file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def load_sample_data(input_path: Path) -> pd.DataFrame:
    """
    Load sample data from a CSV file.
    """
    return pd.read_csv(input_path)


def generate_all_sample_data(output_dir: Path = Path("data/sample_data")) -> dict:
    """
    Generate and save all sample datasets for the three program cards.
    
    Args:
        output_dir: Directory to save CSV files
    
    Returns:
        Dictionary with file paths and datasets
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Education
    edu_df = generate_education_data(n_schools=8, n_classrooms_per_school=5)
    edu_path = save_sample_data(
        edu_df,
        output_dir / "education_bridge_to_basics.csv"
    )
    results["education"] = {"path": edu_path, "df": edu_df, "n_rows": len(edu_df)}
    
    # Health
    health_df = generate_health_data(n_communities=15, n_mothers_per_community=40)
    health_path = save_sample_data(
        health_df,
        output_dir / "health_community_care_loop.csv"
    )
    results["health"] = {"path": health_path, "df": health_df, "n_rows": len(health_df)}
    
    # Agriculture
    ag_df = generate_agriculture_data(n_coops=12, n_farmers_per_coop=18)
    ag_path = save_sample_data(
        ag_df,
        output_dir / "agriculture_smart_water_boost.csv"
    )
    results["agriculture"] = {"path": ag_path, "df": ag_df, "n_rows": len(ag_df)}
    
    return results


if __name__ == "__main__":
    # Generate all sample data when run as a script
    results = generate_all_sample_data()
    
    print("\n✓ Sample data generated successfully!\n")
    for sector, info in results.items():
        print(f"  {sector.capitalize()}:")
        print(f"    Path: {info['path']}")
        print(f"    Rows: {info['n_rows']}")
        print(f"    Columns: {info['df'].shape[1]}\n")
