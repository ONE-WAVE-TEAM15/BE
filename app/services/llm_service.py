import json
from typing import Dict, List

import google.generativeai as genai

from app.core.config import GEMINI_API_KEY


class LLMService:
    """
    LLM service using Google Gemini API.
    Provides interviewer and mentor agent personalities.
    """

    def __init__(self):
        """Initialize Gemini models"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.interviewer_model = genai.GenerativeModel('gemini-2.5-flash')
        self.mentor_model = genai.GenerativeModel('gemini-2.5-flash')

    def format_greeting(
        self,
        user_name: str,
        domain: str,
        project_title: str
    ) -> str:
        """
        Generate a professional Korean greeting for interview start.

        Args:
            user_name: User's name
            domain: Job domain (e.g., "Backend", "Frontend")
            project_title: Project title to discuss

        Returns:
            Korean greeting string
        """
        return f"안녕하세요 {user_name}님, {domain} 직무 면접관입니다. 제출하신 {project_title} 프로젝트에 대해 간략히 설명해 주세요."

    async def generate_interviewer_question(
        self,
        user_answer: str,
        project_context: Dict[str, str],
        history: List[Dict] = None
    ) -> str:
        """
        Generate an aggressive follow-up question as a strict interviewer.

        Args:
            user_answer: The user's latest answer
            project_context: Project information (title, skills_used, content, results)
            history: Optional conversation history

        Returns:
            Korean question string

        Raises:
            Exception: If LLM generation fails
        """
        history = history or []

        # Build conversation history string
        history_text = ""
        if history:
            for msg in history:
                role_kr = "면접관" if msg["role"] == "interviewer" else "지원자"
                history_text += f"{role_kr}: {msg['content']}\n"

        # Construct system prompt
        system_prompt = f"""
당신은 {project_context.get('title', '프로젝트')}의 {project_context.get('skills_used', '기술 스택')}에 대한 엄격한 기술 면접관입니다.

역할:
- 지원자의 기술 역량을 깊이 있게 검증
- 모호한 답변에 대해 구체적인 설명 요구
- 프로젝트의 기술 스택에 대한 심층 질문
- 기술적 의사결정의 근거 확인

프로젝트 정보:
- 제목: {project_context.get('title', 'N/A')}
- 사용 기술: {project_context.get('skills_used', 'N/A')}
- 설명: {project_context.get('content', 'N/A')}
- 결과: {project_context.get('results', 'N/A')}

규칙:
1. 한국어로 질문
2. 한 번에 하나의 질문만
3. 이전 답변을 기반으로 심화 질문
4. 기술 스택의 깊이 있는 이해도 확인
5. 압박감을 주되, 존중하는 태도 유지

이전 대화:
{history_text if history_text else "없음"}

지원자의 답변: {user_answer}

위 답변을 분석하고, 기술적 깊이를 평가할 수 있는 날카로운 후속 질문을 하나 생성하세요. 질문만 출력하고, 다른 설명은 포함하지 마세요.
"""

        try:
            response = self.interviewer_model.generate_content(system_prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"면접관 질문 생성 실패: {str(e)}")

    async def generate_mentor_feedback(
        self,
        interviewer_question: str,
        user_answer: str,
        history: List[Dict] = None
    ) -> Dict[str, any]:
        """
        Generate constructive feedback as a supportive mentor.

        Args:
            interviewer_question: The interviewer's question
            user_answer: The user's answer
            history: Optional conversation history

        Returns:
            Dictionary with 'feedback' (str) and 'tips' (list of str)

        Raises:
            Exception: If LLM generation fails
        """
        history = history or []

        # Build conversation history string
        history_text = ""
        if history:
            for msg in history:
                role_kr = "면접관" if msg["role"] == "interviewer" else "지원자"
                history_text += f"{role_kr}: {msg['content']}\n"

        # Construct system prompt
        system_prompt = f"""
당신은 따뜻하고 경험 많은 기술 멘토입니다.

역할:
- 면접 답변의 강점과 개선점 분석
- 구체적이고 실행 가능한 조언 제공
- 자신감 향상과 기술적 성장 지원
- STAR 기법 등 면접 스킬 코칭

분석 프레임워크:
1. 질문 의도 파악 - 면접관이 무엇을 확인하려 했나?
2. 답변 평가 - 명확성, 구체성, 기술적 정확성
3. 개선 방향 - 어떻게 더 나은 답변을 할 수 있나?
4. 실용적 팁 - 구체적인 개선 방법

규칙:
1. 한국어로 피드백
2. 긍정적이고 건설적인 톤
3. 구체적인 예시 제공
4. 3-5개의 actionable tips
5. 격려와 함께 솔직한 평가
6. 텍스트에 **강조를 위한 마크다운(예: **, __)을 절대 사용하지 마세요.** 모든 답변은 순수 텍스트로만 작성하세요.

이전 대화:
{history_text if history_text else "없음"}

면접관 질문: {interviewer_question}
지원자 답변: {user_answer}

위 답변을 분석하고, 다음 JSON 형식으로 피드백을 제공하세요:
{{
  "feedback": "종합 피드백 (2-3문장)",
  "tips": ["실행 가능한 팁 1", "팁 2", "팁 3"]
}}

JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요.
"""

        try:
            response = self.mentor_model.generate_content(system_prompt)
            response_text = response.text.strip()

            # Clean markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            # Parse JSON response
            feedback_data = json.loads(response_text)

            return {
                "feedback": feedback_data.get("feedback", "피드백을 생성할 수 없습니다."),
                "tips": feedback_data.get("tips", ["답변을 더 구체적으로 말씀해 주세요."])
            }
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            return {
                "feedback": response.text.strip() if response else "피드백을 생성할 수 없습니다.",
                "tips": [
                    "답변을 더 구체적으로 말씀해 주세요.",
                    "기술적 용어를 정확히 사용하세요.",
                    "경험을 구조화해서 설명하세요 (STAR 기법)."
                ]
            }
        except Exception as e:
            raise Exception(f"멘토 피드백 생성 실패: {str(e)}")
