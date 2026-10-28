from pydantic import BaseModel, Field

from backend.app.core.config import settings
from backend.app.services.ai_client import client

class ProjectAnalysis(BaseModel):
    name: str | None = None
    technologies: list[str] = Field(default_factory=list)
    description: str | None = None

class EducationAnalysis(BaseModel):
    degree: str | None = None
    field: str | None = None
    institution: str | None = None

class ResumeAnalysis(BaseModel):
    skills: list[str] = Field(default_factory=list)
    experience_years: float | None = None
    projects: list[ProjectAnalysis] = Field(
        default_factory=list
    )
    education: list[EducationAnalysis] = Field(
        default_factory=list
    )
    summary: str | None = None

def analyze_resume_with_ai(
    resume_text: str,
) -> ResumeAnalysis:

    prompt = f"""
You are a resume analysis system.

Analyze the resume below and return ONLY valid JSON.

Do not return markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use exactly this JSON structure:

{{
    "skills": [],
    "experience_years": null,
    "projects": [
        {{
            "name": "",
            "technologies": [],
            "description": null
        }}
    ],
    "education": [
        {{
            "degree": null,
            "field": null,
            "institution": null
        }}
    ],
    "summary": null
}}

Rules:

- Extract only information supported by the resume.
- Never invent skills, experience, projects, education,
  companies, technologies, or other information.
- For skills, include skills explicitly listed or clearly
  demonstrated.
- For experience_years, use the total professional
  experience only when it is explicitly stated or can be
  reliably calculated.
- If experience cannot be determined reliably, use null.
- If there are no projects, return an empty list.
- If there is no education information, return an empty list.
- If there is no summary-worthy information, use null.

Resume:

{resume_text}
"""

    response = client.chat.completions.create(
        model=settings.ai_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured information "
                    "from resumes. Return valid JSON only."
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
            "AI returned an empty response."
        )

    import json

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "AI returned invalid JSON."
        ) from exc

    return ResumeAnalysis.model_validate(data)