
from core.database import (
    initialize_database,
    add_complaint,
    get_all_complaints,
    get_complaint_by_id,
    update_complaint_status
)

print("=" * 45)
print("KURAL GRIEVANCE - DATABASE TEST")
print("=" * 45)

# Create the database and table
initialize_database()
print("\nDatabase initialized successfully.")

# Use fictional test complaint data
test_complaint = (
    "எங்கள் பகுதியில் குடிநீர் வரவில்லை."
)

test_analysis = {
    "detected_language": "Tamil",
    "translated_complaint": "Drinking water is unavailable in our area.",
    "department": "Water",
    "priority_score": 70,
    "priority_reason": "Water shortage affects daily basic needs."
}

# Save the complaint
complaint_id = add_complaint(
    test_complaint,
    test_analysis
)

print("\nComplaint saved successfully!")
print("Generated Complaint ID:", complaint_id)

# Retrieve the complaint
saved_complaint = get_complaint_by_id(complaint_id)

print("\nRetrieved Complaint:")
print(saved_complaint)

# Update complaint status
update_complaint_status(
    complaint_id,
    "Under Review"
)

print("\nUpdated Status:")
updated_complaint = get_complaint_by_id(complaint_id)
print(updated_complaint["status"])

# Retrieve all complaints
all_complaints = get_all_complaints()

print("\nTotal complaints in database:", len(all_complaints))

print("\nSUCCESS! Database is working.")
