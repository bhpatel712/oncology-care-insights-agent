# Setup Guide

## Prerequisites

- Azure subscription (free account at portal.azure.com)
- Python 3.10+
- Azure CLI (`az`) installed
- VS Code with Python + Azure extensions

## 1. Clone the repo

```bash
git clone https://github.com/<your-username>/oncology-care-insights-agent.git
cd oncology-care-insights-agent
```

## 2. Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure environment variables

```bash
cp .env.example .env
# Fill in your Azure resource values in .env
```

## 4. Deploy Azure infrastructure

```bash
cd infra
az deployment group create \
  --resource-group oncology-agent-rg \
  --template-file main.bicep \
  --parameters @parameters.json
```

## 5. Run the indexer

```bash
python src/indexer/run_indexer.py
```

## 6. Start the frontend

```bash
streamlit run frontend/app.py
```
