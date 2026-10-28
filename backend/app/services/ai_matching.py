import json

from pydantic import BaseModel, Field

from backend.app.core.config import settings
from backend.app.services.ai_client import client


class SkillEvidence(BaseModel):
    skill: str
    matched: bool
    evidence: str | None = None


class SemanticMatchAnalysis(BaseModel):
    overall_relevance: float = Field(
        ge=0,
        le=100,
    )
    skill_evidence: list[SkillEvidence] = Field(
        default_factory=list
    )
    strengths: list[str] = Field(
        default_factory=list
    )
    concerns: list[str] = Field(
        default_factory=list
    )
    explanation: str | None = None


def analyze_semantic_match(
    *,
    job_description: str,
    required_skills: str,
    resume_text: str,
) -> SemanticMatchAnalysis:

    prompt = f"""
You are an AI resume screening system.

Compare the job requirements with the candidate resume.

Return ONLY valid JSON.
Do not return markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "overall_relevance": 0,
    "skill_evidence": [
        {{
            "skill": "",
            "matched": false,
            "evidence": null
        }}
    ],
    "strengths": [],
    "concerns": [],
    "explanation": null
}}

Rules:

1. overall_relevance must be a number from 0 to 100.

2. Evaluate whether the candidate actually demonstrates
   the required skills.

3. Consider semantic equivalents.
   For example:
   - "RESTful backend services" can support REST API experience.
   - "relational database development" can support SQL/database
     experience when the resume provides sufficient evidence.

4. Do NOT assume a skill simply because a related technology
   appears.

5. Every matched skill must have evidence from the resume.

6. If there is no evidence for a required skill:
   - matched must be false
   - evidence must be null

7. Do not invent projects, experience, skills, employers,
   education, or achievements.

8. strengths should contain only strengths supported by the resume.

9. concerns should contain only genuine gaps or weaknesses
   relevant to the job.

10. Keep the explanation concise and factual.

JOB DESCRIPTION:

{job_description}

REQUIRED SKILLS:

{required_skills}

CANDIDATE RESUME:

{resume_text}
"""

    response = client.chat.completions.create(
        model=settings.ai_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise resume-to-job "
                    "semantic matching system. "
                    "Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "AI semantic matcher returned an empty response."
        )

    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "AI semantic matcher returned invalid JSON."
        ) from exc

    return SemanticMatchAnalysis.model_validate(data)