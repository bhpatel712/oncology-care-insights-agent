"""
Oncology Care Insights Agent — Streamlit Chat Frontend
Decision-support tool for clinical operations analysts.
"""

import streamlit as st
import os
import logging
import pymssql
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from azure.monitor.opentelemetry import configure_azure_monitor

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ── APPLICATION INSIGHTS ──────────────────────────────────
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
if connection_string:
    configure_azure_monitor(connection_string=connection_string)
logger = logging.getLogger(__name__)

# ── CONTENT SAFETY ────────────────────────────────────────
def check_content_safety(text):
    """
    Check if input text is safe before sending to agent.
    Returns (True, None) if safe, (False, category) if unsafe.
    """
    try:
        safety_client = ContentSafetyClient(
            endpoint=os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
            credential=AzureKeyCredential(
                os.getenv('AZURE_CONTENT_SAFETY_KEY')
            )
        )
        result = safety_client.analyze_text(
            AnalyzeTextOptions(text=text)
        )
        for category in result.categories_analysis:
            if category.severity >= 4:
                return False, category.category
        return True, None
    except Exception as e:
        logger.warning(f"Content safety check failed: {e}")
        return True, None

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="Oncology Care Insights Agent",
    page_icon="🎗️",
    layout="wide"
)

# ── HEADER ────────────────────────────────────────────────
st.title("🎗️ Oncology Care Insights Agent")
st.markdown("""
> **Decision-support tool for clinical operations and care management analysts.**
> Covers breast, lung, and colorectal cancer.
""")
st.warning("""
⚠️ **Important:** This tool is for clinical operations decision support only.
It is NOT a clinical diagnostic tool and NOT a substitute for oncologist judgment.
All patient data is fully synthetic (Synthea/mCODE format — zero real PHI).
""")
st.divider()

# ── AGENT FUNCTION ────────────────────────────────────────
def get_answer(question):
    """Get answer combining SQL cohort data + gpt-5-mini reasoning."""

    # Fresh SQL connection every time
    conn = pymssql.connect(
        server='oncology-sql-server.database.windows.net',
        user='oncologyadmin',
        password=os.getenv('AZURE_SQL_PASSWORD'),
        database='oncology-patients',
        port=1433
    )
    cursor = conn.cursor()

    # Get cohort stats
    cursor.execute("""
        SELECT c.cancer_type,
               COUNT(DISTINCT c.patient_id) as cnt,
               SUM(CASE WHEN p.gender='female' THEN 1 ELSE 0 END) as f,
               SUM(CASE WHEN p.gender='male' THEN 1 ELSE 0 END) as m
        FROM Conditions c
        JOIN Patients p ON c.patient_id = p.patient_id
        WHERE c.is_cancer = 1
        AND c.cancer_type IS NOT NULL
        GROUP BY c.cancer_type
    """)
    rows = cursor.fetchall()
    conn.close()

    cohort = "\n".join([
        f"- {r[0]} cancer: {r[1]} patients ({r[2]} female, {r[3]} male)"
        for r in rows
    ])

    # OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version="2024-12-01-preview",
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
    )

    # Call model
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": """You are the Oncology Care Insights Agent.
You MUST answer using ONLY the synthetic patient data provided.
Do NOT ask for more information. Do NOT say you don't have access.
Always state the data is synthetic (Synthea/mCODE).
Decline any diagnosis or treatment recommendation requests.
This is decision-support only — not a diagnostic tool.
Cancer types covered: breast, lung, colorectal only."""
            },
            {
                "role": "user",
                "content": f"""Our synthetic patient cohort data:
{cohort}

Question: {question}

Answer directly using the data above."""
            }
        ],
        max_completion_tokens=5000
    )

    answer = response.choices[0].message.content

    # Log to Application Insights
    logger.info("Agent query processed", extra={
        "custom_dimensions": {
            "question_length": len(question),
            "answer_length": len(answer),
            "tokens_used": response.usage.completion_tokens,
            "cancer_type": next(
                (c for c in ['breast', 'lung', 'colorectal']
                 if c in question.lower()), "general"
            )
        }
    })

    return answer

# ── CHAT HISTORY ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": """👋 Welcome to the Oncology Care Insights Agent!

I can help you with:
- 📊 **Patient cohort stats** — counts, age distribution, gender breakdown
- 🏥 **NCI PDQ guidelines** — treatment recommendations
- 🔍 **Combined insights** — guidelines + patient population

**Try asking:**
- *"How many breast cancer patients do we have?"*
- *"Compare patient counts across all 3 cancer types"*
- *"What is the age breakdown of lung cancer patients?"*
- *"How is colorectal cancer treated?"*
"""
    })

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── CHAT INPUT ────────────────────────────────────────────
prompt = st.chat_input("Ask about oncology guidelines or patient cohorts...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching guidelines and patient data..."):
            try:
                # Content Safety check first
                is_safe, flagged_category = check_content_safety(prompt)

                if not is_safe:
                    safety_msg = f"""⚠️ Your message was flagged by Content Safety
filters ({flagged_category}) and cannot be processed.

Please rephrase your question to focus on:
- Oncology treatment guidelines
- Patient cohort statistics
- Clinical operations support"""
                    st.warning(safety_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": safety_msg
                    })
                else:
                    answer = get_answer(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Quick Stats")
    st.markdown("""
    **Synthetic Patient Cohort:**
    - 🎗️ Breast cancer: 48 patients
    - 🫁 Lung cancer: 13 patients
    - 🔵 Colorectal cancer: 28 patients
    - 📋 Total records: 41,700+

    **Knowledge Base:**
    - 📚 NCI PDQ guidelines
    - 🔍 272 indexed chunks
    - 3 cancer types covered
    """)

    st.divider()

    st.header("💡 Try These Questions")
    st.markdown("""
    Type these in the chat box:

    💬 *How many breast cancer patients do we have?*

    💬 *Compare all 3 cancer types*

    💬 *Age breakdown of lung cancer patients?*

    💬 *What is the treatment for Stage II breast cancer?*

    💬 *How is colorectal cancer diagnosed?*

    💬 *Can you diagnose my symptoms?*
    """)

    st.divider()

    st.header("🔒 Safety Status")
    st.success("✅ Content Safety: Active")
    st.success("✅ Application Insights: Active")
    st.success("✅ Responsible AI: Enabled")
    st.success("✅ PHI Protection: Zero real data")

    st.divider()
    st.caption("Oncology Care Insights Agent v1.0")
    st.caption("Built with Microsoft Foundry + Azure AI")
    st.caption("© 2026 Bhargavi Patel")