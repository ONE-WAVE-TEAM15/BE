import json
from app.utils.ai_analysis import analyze_portfolio

def test_ai_analysis():
    # 1. Load Dummy Data
    with open("user_dummy.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
    
    with open("project_dummy.json", "r", encoding="utf-8") as f:
        project_data = json.load(f)

    with open("job_dummy.json", "r", encoding="utf-8") as f:
        job_data = json.load(f)

    print("--- AI Analysis Testing Start ---")
    print(f"Target Job: {job_data['company']} - {job_data['title']}")
    print("Sending data to Gemini API...")

    # 2. Call analyze_portfolio
    result = analyze_portfolio(user_data, project_data, job_data)

    # 3. Print Result
    print("\n--- AI Analysis Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n--- End of Test ---")

if __name__ == "__main__":
    test_ai_analysis()
