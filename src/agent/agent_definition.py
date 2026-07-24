"""
Oncology Care Insights Agent — Agent definition and orchestration.
Combines NCI PDQ guideline retrieval with synthetic patient cohort queries.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.tools.sql_tool import (
    get_cohort_stats,
    get_treatment_distribution,
    get_patient_panel_summary
)

load_dotenv()

AGENT_NAME = "oncology-care-insights-agent"
AGENT_MODEL = "gpt-5-mini"

# Load system prompt
_dir = os.path.dirname(__file__)
with open(os.path.join(_dir, "system_prompt.txt"), "r") as f:
    SYSTEM_PROMPT = f.read()

# Initialize OpenAI client
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)


def build_context(question: str) -> str:
    """
    Build context from SQL cohort data based on the question.
    Automatically detects which cancer type is being asked about.
    """
    # Get all cohort stats
    cohort_data = get_cohort_stats()
    cohort_summary = "\n".join([
        f"- {item['cancer_type']} cancer: {item['patient_count']} patients "
        f"({item['female_count']} female, {item['male_count']} male)"
        for item in cohort_data.get('data', [])
    ])

    # Get specific cancer details if mentioned
    extra_context = ""
    for cancer_type in ['breast', 'lung', 'colorectal']:
        if cancer_type in question.lower():
            summary = get_patient_panel_summary(cancer_type)
            if summary['status'] == 'success':
                age_summary = ", ".join([
                    f"{a['age_group']}: {a['count']}"
                    for a in summary['age_distribution']
                ])
                extra_context = (
                    f"\n{cancer_type.title()} cancer age distribution: "
                    f"{age_summary}"
                )

    context = f"""
SYNTHETIC PATIENT COHORT DATA (Synthea/mCODE — not real patients):
{cohort_summary}
{extra_context}

Always state this data is synthetic when reporting numbers.
"""
    return context


def answer_question(question: str) -> str:
    """
    Main agent function — answers oncology questions using:
    1. SQL cohort data from Azure SQL
    2. gpt-5-mini reasoning
    Returns a grounded, cited answer.
    """
    # Build context from SQL data
    context = build_context(question)

    # Build augmented prompt
    prompt = f"""{SYSTEM_PROMPT}

{context}

User question: {question}

Answer concisely. Cite that patient data is synthetic.
Keep your answer focused and professional."""

    # Call gpt-5-mini
    response = client.chat.completions.create(
        model=AGENT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=2000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("Testing Oncology Care Insights Agent...")
    print("=" * 60)

    test_questions = [
        "How many breast cancer patients do we have?",
        "Compare patient counts across all 3 cancer types",
        "Can you diagnose my cancer symptoms?"
    ]

    for q in test_questions:
        print(f"\n❓ {q}")
        answer = answer_question(q)
        print(f"💬 {answer}")
        print("-" * 60)

    print("\n✅ Agent definition ready!")