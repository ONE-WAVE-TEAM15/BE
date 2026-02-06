import json
from app.utils.ai_analysis import analyze_portfolio

def test_ai_analysis():
    data_dir = "dummy_data"
    with open(f"{data_dir}/user_dummy.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
    
    with open(f"{data_dir}/project_dummy.json", "r", encoding="utf-8") as f:
        project_data = json.load(f)

    with open(f"{data_dir}/job_dummy.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
        job_data = jobs[0] if isinstance(jobs, list) else jobs

    print("--- AI Analysis Testing Start ---")
    print(f"Target Job: {job_data['company']} - {job_data['title']}")
    print("Sending data to Gemini API...")

    result = analyze_portfolio(user_data, project_data, job_data)

    print("\n--- AI Analysis Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n--- End of Test ---")

if __name__ == "__main__":
    test_ai_analysis()
