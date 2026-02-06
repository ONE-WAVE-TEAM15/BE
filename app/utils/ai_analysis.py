import json
import os
from pathlib import Path
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_portfolio(user_data: dict, project_data: dict, job_data: dict) -> str:
    """
    Analyzes the match between a user's profile/project and a job description using Google Gemini API.
    Also recommends training programs based on missing skills using data from program_dummy.json.
    
    Returns:
        str: The analysis result from Gemini (in Korean).
    """
    if not GEMINI_API_KEY:
        return "Gemini API Key is missing."

    client = Client(api_key=GEMINI_API_KEY)

    # Load programs from program_dummy.json
    programs = []
    try:
        base_path = Path(__file__).resolve().parent.parent.parent
        json_path = base_path / "program_dummy.json"
        
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                programs = json.load(f)
            
    except Exception as e:
        print(f"Error loading program_dummy.json: {e}")

    try:
        # Format programs for the prompt with full details
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
        
        # Using gemini-flash-latest for better quota availability
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        
        # Parse the JSON response
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse AI response as JSON",
                "raw_response": response.text
            }
            
    except Exception as e:
        return {"error": f"Error analyzing job match: {str(e)}"}
{
  "skill_match": "후보자는 Java, Spring Boot, MySQL 등 기본적인 백엔드 개발 스택을 보유하고 있으며, 프로젝트에서도 해당 기술 스택을 활용했습니다. 이는 직무의 핵심 언어 요구사항과 일치합니다. 그러나 요구 기술 목록에 포함된 AWS(클라우드), Docker, Kubernetes(컨테이너/MSA 운영), Redis(캐싱), Kafka(메시지 큐)와 같은 차세대 플랫폼 구축에 필수적인 기술들이 후보자의 스킬셋 및 프로젝트 경험에 명확히 포함되어 있지 않아 상당한 격차가 존재합니다.",
  "fit_evaluation": "후보자는 '대용량 데이터 처리'와 'MSA 경험'에 대한 관심 및 경험(Survey 기준)을 표명하고 있어 직무의 요구사항(MSA 환경, 대규모 트래픽 처리)과 방향성 은 일치합니다. 하지만 실제 프로젝트 경험은 Spring Boot와 JPA를 사용한 기본적인 CRUD 게시판 수준에 머물러 있어, 요구되는 '차세대 클라우드 플랫폼 구축' 및 '대규모 아키텍 처 설계' 역량을 입증하기에는 매우 부족합니다. 신입 개발자로서의 잠재력은 있으나, 해당 고난이도 포지션에 즉시 투입되기에는 기술적 깊이와 실무 경험이 부족합니다.",
  "missing_competencies": [
    "AWS 기반 클라우드 환경 구축 및 운영 경험",
    "Docker 및 Kubernetes를 활용한 MSA 배포 및 관리",
    "Redis를 활용한 고성능 데이터 캐싱 또는 세션 관리",
    "Kafka를 활용한 대규모 이벤트 및 메시지 처리 시스템 구축",
    "MSA 아키텍처 설계 및 구현 (CRUD 수준 이상의 복잡성)"
  ],
  "overall_score": 60,
  "recommended_programs": [
    {
      "title": "스프린트 백엔드 마스터 부트캠프 4기",
      "reason": "Docker와 Kubernetes 스킬을 익혀 클라우드 환경에서 요구되는 컨테이너화 및 배포/운영 역량을 향상시킬 수 있습니다."
    },
    {
      "title": "MSA 기반 이커머스 플랫폼 구축 프로젝트",
      "reason": "실제 MSA 환경 구축 경험과 함께 Kafka, Docker 활용 능력을 습득하여 가장 크게 부족한 MSA 및 분산 시스템 실무 경험을 보완할 수 있습니다."
    },
    {
      "title": "2026 제2회 백엔드 성능 최적화 경진대회",
      "reason": "Redis 사용 경험을 쌓아 고성능 환경 구축에 필수적인 캐싱 및 성능 최적화 역량을 확보할 수 있습니다."
    }
  ]
}