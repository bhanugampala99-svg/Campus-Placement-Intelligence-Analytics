"""
Campus Placement Intelligence Analytics
---------------------------------------
Python script for data loading, cleaning, and exploratory analysis.

Tools: pandas, numpy, matplotlib, seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# -------------------------
# 1. Load Data
# -------------------------

data_path = data_path = r"C:\Users\bbhan\Desktop\Campus Placement Intelligence Analytics\data\placements_data.csv"
df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nColumn dtypes:\n", df.dtypes)

# -------------------------
# 2. Basic Data Cleaning
# -------------------------

# Trim strings
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].astype(str).str.strip()

# Replace empty or 'nan' in placement_status and company_type
df["placement_status"] = df["placement_status"].replace({"nan": np.nan, "": np.nan})
df["company_type"] = df["company_type"].replace({"nan": np.nan, "": np.nan})

# CTC: ensure numeric
df["ctc_lakhs"] = pd.to_numeric(df["ctc_lakhs"], errors="coerce")

# For not placed students, ensure CTC is 0 or NaN
df.loc[df["placement_status"] == "Not Placed", "ctc_lakhs"] = 0

# -------------------------
# 3. Feature Engineering
# -------------------------

# CGPA bands
def cgpaband(x):
    if x >= 8.0:
        return "8.0+"
    elif x >= 7.0:
        return "7.0-7.9"
    elif x >= 6.0:
        return "6.0-6.9"
    else:
        return "<6.0"

df["cgpa_band"] = df["cgpa"].apply(cgpaband)

# Skill count
df["skill_count"] = df["skills"].apply(
    lambda x: len([s for s in str(x).split(",") if s.strip() != ""]) if pd.notna(x) else 0
)

# -------------------------
# 4. Summary Statistics
# -------------------------

print("\nSummary statistics for numeric columns:\n", df.describe())

placement_rate = (df["placement_status"] == "Placed").mean() * 100
print(f"\nOverall Placement Rate: {placement_rate:.2f}%")

avg_ctc_placed = df.loc[df["placement_status"] == "Placed", "ctc_lakhs"].mean()
print(f"Average CTC (Placed students): {avg_ctc_placed:.2f} lakhs")

# Placement rate by branch
placement_by_branch = (
    df.groupby("branch")["placement_status"]
    .apply(lambda x: (x == "Placed").mean() * 100)
    .sort_values(ascending=False)
)
print("\nPlacement rate by branch (%):\n", placement_by_branch)

# Average CTC by college tier (placed students)
avg_ctc_by_tier = (
    df.loc[df["placement_status"] == "Placed"]
    .groupby("college_tier")["ctc_lakhs"]
    .mean()
)
print("\nAverage CTC by college tier (placed students):\n", avg_ctc_by_tier)

# -------------------------
# 5. Simple Visualizations
# -------------------------

# Placement rate by branch
plt.figure()
sns.barplot(x=placement_by_branch.index, y=placement_by_branch.values)
plt.title("Placement Rate by Branch")
plt.xlabel("Branch")
plt.ylabel("Placement Rate (%)")
plt.tight_layout()
plt.savefig("../screenshots/placement_rate_by_branch.png")
plt.close()

# CTC distribution for placed students
plt.figure()
sns.histplot(df.loc[df["placement_status"] == "Placed", "ctc_lakhs"], kde=True)
plt.title("CTC Distribution (Placed Students)")
plt.xlabel("CTC (lakhs)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../screenshots/ctc_distribution.png")
plt.close()

print("\nPlots saved to ../screenshots/")
