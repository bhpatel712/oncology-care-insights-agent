# Architecture: Oncology Care Insights Agent

## Overview

A Microsoft Foundry Agent Service application with two tool-callable data sources:
1. **Azure AI Search** — vector + semantic hybrid index over NCI PDQ cancer treatment summaries
2. **Azure SQL Database** — synthetic oncology patient cohort (Synthea/mCODE format)

## Component diagram

See architecture diagram in project planning docs.

## Services used

| Service | Purpose | Tier |
|---|---|---|
| Microsoft Foundry | Agent hosting, model deployment | Pay-as-you-go |
| gpt-5-mini | Chat + reasoning model | Pay-as-you-go tokens |
| text-embedding-3-small | Embedding model for indexing | Pay-as-you-go tokens |
| Azure AI Search | Guideline retrieval (vector + semantic) | Free tier |
| Azure SQL Database | Synthetic patient cohort queries | Basic DTU (~$5/mo) |
| Azure Functions | SQL tool wrapper (parameterized queries) | Consumption plan |
| Azure Key Vault | Secrets management | Standard |
| Azure Content Safety | Content filtering | Free tier |
| Application Insights | Tracing, token usage, latency | Pay-as-you-go |
| Azure Container Apps | Front-end hosting | Consumption plan |
| Microsoft Entra ID | Managed identity / keyless auth | Included |

> **Model note:** Originally planned around GPT-4o and text-embedding-3-large. Switched to gpt-5-mini (GPT-4o deprecated for new accounts) and text-embedding-3-small (text-embedding-3-large unavailable on free quota) — see `docs/progress.md` for the full decision log.

## Data flow

1. User types a question in the chat UI
2. Frontend sends the message to the backend API
3. Backend calls Foundry Agent Service via `azure-ai-projects` SDK
4. Agent reasons over the question and decides which tool(s) to call:
   - **search_guidelines** → queries Azure AI Search (RAG retrieval)
   - **query_patient_cohort** → calls Azure Function → parameterized SQL on Azure SQL
5. Agent assembles a grounded, cited answer and returns it
6. Frontend displays the answer with citations and tool call trace

## Security

- All service-to-service auth uses managed identity (no secrets in code)
- API keys stored in Key Vault only
- Content Safety filters applied to all inputs and outputs
- All data is synthetic — zero PHI
