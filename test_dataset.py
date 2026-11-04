
import pandas as pd

print("=" * 45)
print("KURAL GRIEVANCE - DATASET TEST")
print("=" * 45)

# Load the sample complaints dataset
df = pd.read_csv("data/sample_complaints.csv")

print("\nDataset loaded successfully!")

# Display basic information
print("\nTotal complaints:", len(df))

print("\nComplaints by language:")
print(df["language"].value_counts())

print("\nComplaints by department:")
print(df["expected_department"].value_counts())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Display a few examples
print("\nFirst 5 complaints:")
print(df.head().to_string(index=False))

# Validate the dataset
assert len(df) == 30, "Expected exactly 30 complaints."
assert df["complaint_text"].notnull().all(), "Some complaints are empty."
assert df["expected_department"].notnull().all(), "Some departments are missing."

print("\nSUCCESS! Dataset is working correctly.")
