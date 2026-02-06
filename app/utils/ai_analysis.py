import json
import os
from pathlib import Path
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_portfolio(user_data: dict, project_data: dict, job_data: dict) -> dict:
    if not GEMINI_API_KEY:
        return "Gemini API Key is missing."

    client = Client(api_key=GEMINI_API_KEY)

    programs = []
    try:
        base_path = Path(__file__).resolve().parent.parent.parent
        json_path = base_path / "dummy_data" / "program_dummy.json"
        
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                programs = json.load(f)
            
    except Exception as e:
        print(f"Error loading program_dummy.json: {e}")

    try:
        if programs:
            programs_text = json.dumps(programs, ensure_ascii=False, indent=2)
        else:
            programs_text = "No training programs available at the moment."

        prompt = f"""
        Role: You are an expert HR consultant and Technical Recruiter.
        
        Task: Analyze the fit between a candidate's profile/project experience and a specific job opening.
        
        Please compare the following information:
        
        === CANDIDATE PROFILE ===
        [Self Summary]
        {user_data.get('self_summary', 'N/A')}
        
        [Survey / Career Interests]
        {user_data.get('survey_text', 'N/A')}
        
        [Candidate Skills]
        {user_data.get('skills', 'N/A')}
        
        === PROJECT EXPERIENCE ===
        [Project Content]
        {project_data.get('content', 'N/A')}
        
        [Project Tech Stack]
        {project_data.get('skills_used', 'N/A')}
        
        === JOB OPENING ===
        [Job Description]
        {job_data.get('description', 'N/A')}
        
        [Required Skills]
        {job_data.get('skills_required', 'N/A')}
        
        === AVAILABLE TRAINING PROGRAMS (JSON) ===
        {programs_text}
        
        ---
        
        Analysis Instructions:
        1. **Skill Match Analysis**: Compare [Candidate Skills] & [Project Tech Stack] against [Required Skills]. Identify matched skills and specifically highlight **missing skills**.
        2. **Fit Evaluation**: Evaluate if the [Project Content] and [Self Summary] align with the responsibilities described in [Job Description]. Determine if the candidate is a good fit for the role.
        3. **Missing Competencies**: Clearly list the key competencies or skills the candidate is lacking for this specific role.
        4. **Overall Score**: Give a fit score out of 100 based on the analysis.
        5. **Recommended Programs**: Check the [AVAILABLE TRAINING PROGRAMS] list. If a program's listed skills cover **at least one** of the identified [Missing Competencies/Skills], recommend that program. 
           **IMPORTANT**: For each recommendation, return the ENTIRE JSON object of the program as found in the input list, and add a "recommendation_reason" field explaining why it was chosen.

        Output Format:
        Return ONLY a JSON object with the following keys. The values should be in Korean:
        - "skill_match": "Detailed skill match analysis string"
        - "fit_evaluation": "Detailed fit evaluation string"
        - "missing_competencies": ["List", "of", "missing", "competencies"]
        - "overall_score": 85 (as an integer)
        - "recommended_programs": [{{ ...full_program_object..., "recommendation_reason": "Reason for recommendation" }}]
        """
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse AI response as JSON",
                "raw_response": response.text
            }
            
    except Exception as e:
        return {"error": f"Error analyzing job match: {str(e)}"}