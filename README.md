# 🎗️ Oncology Care Insights Agent

> **An agent-based AI application on Microsoft Foundry that helps clinical-ops analysts query NCI oncology guidelines and synthetic patient cohorts in plain language — deployed on Azure with RAG, tool-calling, and responsible AI guardrails.**

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![Azure](https://img.shields.io/badge/Azure-Microsoft%20Foundry-blue)](https://ai.azure.com)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Project Overview

The **Oncology Care Insights Agent** is a clinical operations decision-support application built for care management analysts. It enables users to ask plain-language questions about cancer treatment guidance and patient population patterns.

**Cancer types covered:** Breast · Lung · Colorectal

**Data sources:**
- 📚 **NCI PDQ cancer treatment summaries** (public domain) — for clinical guideline knowledge
- 🏥 **Synthea/mCODE synthetic patient records** (zero real PHI) — for cohort-level population insights

> ⚠️ **Decision-support only** — not a clinical diagnostic tool. All patient data is fully synthetic.

---

## 🏗️ Architecture

User (Care-ops Analyst)
↓
Streamlit Chat Interface
↓
Microsoft Foundry Agent Service (GPT-5-mini)
↓ ↓
Azure AI Search Azure SQL Database
(NCI PDQ Guidelines) (Synthea/mCODE Patients)
272 indexed chunks 95 cancer patients
41,700+ clinical records


---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| **AI Platform** | Microsoft Foundry |
| **Language Model** | GPT-5-mini |
| **Embedding Model** | text-embedding-3-small |
| **Vector Search** | Azure AI Search (hybrid) |
| **Patient Database** | Azure SQL Database |
| **Safety** | Azure Content Safety |
| **Observability** | Application Insights |
| **Frontend** | Streamlit |
| **Language** | Python 3.14 |
| **IaC** | Bicep |

---

## 📊 Key Stats

| Metric | Value |
|---|---|
| Cancer types | Breast, Lung, Colorectal |
| Synthetic patients | 95 |
| Clinical records | 41,700+ |
| NCI PDQ chunks | 272 |
| Avg tokens/chunk | 593 |
| Eval score | 91% overall |
| Guardrail pass rate | 90% |

---

## 🎯 Evaluation Results

| Category | Score |
|---|---|
| RAG-only (guideline retrieval) | 93% |
| SQL-only (cohort queries) | 90% |
| Combined (guidelines + cohort) | 90% |
| Adversarial (guardrails) | 90% |
| **Overall** | **91%** |

---

## 🔒 Responsible AI

This project implements Microsoft's Responsible AI principles:

- ✅ **Privacy & Security** — Zero real PHI, synthetic data only
- ✅ **Reliability & Safety** — Content Safety filters active
- ✅ **Transparency** — Every answer cites its source
- ✅ **Accountability** — "Decision-support only" guardrails enforced
- ✅ **Fairness** — Diverse synthetic patient demographics

---

## 🛠️ Setup

### Prerequisites
- Azure subscription
- Python 3.10+
- Azure CLI

### Installation

```bash
# Clone the repo
git clone https://github.com/bhpatel712/oncology-care-insights-agent.git
cd oncology-care-insights-agent

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in your Azure credentials in .env
```

### Run the app

```bash
streamlit run frontend/app.py
```

---

## 📁 Project Structure

oncology-care-insights-agent/
├── frontend/app.py # Streamlit chat interface
├── src/
│ ├── agent/
│ │ ├── agent_definition.py # Agent orchestration
│ │ └── system_prompt.txt # Responsible AI guardrails
│ └── tools/
│ └── sql_tool.py # Patient cohort queries
├── data/
│ ├── raw/guidelines/ # NCI PDQ guideline text
│ └── eval/ # Evaluation questions + results
├── notebooks/ # Data exploration + ETL
├── tests/test_tools.py # Automated evaluation (91%)
├── infra/main.bicep # Azure IaC templates
└── .github/workflows/ # CI/CD pipeline


---

## 🎓 AI-103 Alignment

This project was built alongside studying for the **Microsoft AI-103** exam
(Developing AI Apps and Agents on Azure):

| Domain | Coverage |
|---|---|
| Domain 1 — Plan & manage | ✅ Provisioning, RBAC, managed identity, cost management |
| Domain 2 — Generative AI | ✅ RAG pipeline, agent + tool calling, evaluation |
| Domain 5 — Info extraction | ✅ NCI PDQ chunking + indexing |

---

## ⚠️ Known Limitations

- Synthea breast cancer module lacks full pathologic staging and genomics
- Cohort queries reflect synthetic population patterns only
- Designed for analyst/ops audience — not for patient-facing use
- gpt-5-mini used instead of GPT-4o due to free account quota limits

---

## 👩‍💻 Author

**Bhargavi Patel**
Senior Data Analyst → AI/ML Engineer
11+ years SQL, Power BI, ETL, healthcare/clinical ops

[![GitHub](https://img.shields.io/badge/GitHub-bhpatel712-black)](https://github.com/bhpatel712)

---

*Built with Microsoft Foundry · Azure AI Search · Azure SQL · Python · Streamlit*