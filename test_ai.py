
from core.ai_pipeline import analyze_complaint
import json

print("=" * 50)
print("KURAL GRIEVANCE - GEMINI AI TEST")
print("=" * 50)

complaint = "எங்கள் பகுதியில் கடந்த மூன்று நாட்களாக குடிநீர் வரவில்லை."

print("\nOriginal Complaint:")
print(complaint)

print("\nSending complaint to Gemini...")

try:
    result = analyze_complaint(complaint)

    print("\nAI ANALYSIS RESULT")
    print("-" * 50)

    print(json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    ))

    print("\nTEST SUMMARY")
    print("-" * 50)
    print("Language:", result["detected_language"])
    print("Department:", result["department"])
    print("Priority:", result["priority_score"], "/ 100")
    print("Reason:", result["priority_reason"])

    print("\nSUCCESS! Gemini is working.")

except Exception as error:
    print("\nTEST FAILED!")
    print("Error:", error)
    print("\nPlease share the error message with me.")

