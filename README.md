# Oncology Care Insights Agent

A care-ops/clinical-analyst-facing AI agent built on Microsoft Foundry that answers questions combining NCI oncology guidelines with synthetic patient population data.

**Cancer types:** Breast · Lung · Colorectal
**Data:** NCI PDQ summaries (public domain) + Synthea/mCODE synthetic patients (zero PHI)
**Stack:** Microsoft Foundry · Azure AI Search · Azure SQL Database · Azure Functions · Python

> ⚠️ This is a decision-support tool for clinical operations and data analysts.
> It is not a clinical diagnostic tool and is not a substitute for oncologist judgment.
> All patient data is fully synthetic.

## Architecture

See [`docs/architecture.md`](docs/architecture.md)

## Setup

See [`docs/setup.md`](docs/setup.md)

## Project structure

```
oncology-care-insights-agent/
├── docs/               # Architecture, setup, scope, eval results
├── infra/              # Bicep templates for all Azure resources
├── data/               # Raw + processed guideline data, eval question sets
├── src/
│   ├── agent/          # Agent definition, system prompt, tool registration
│   ├── tools/          # Azure Function SQL tool wrappers
│   ├── indexer/        # NCI PDQ chunking + embedding + indexing pipeline
│   └── api/            # Backend API connecting frontend to agent
├── frontend/           # Streamlit or React chat interface
├── notebooks/          # Exploration, ETL validation, eval analysis
├── tests/              # Unit + integration tests
└── .github/workflows/  # CI/CD pipelines
```

## Known limitations

- Synthea breast cancer module does not capture full pathologic staging or genomics
- Cohort queries reflect synthetic population patterns, not real clinical data
- Designed for analyst/ops audience — not for point-of-care or patient-facing use
