# Oncology Care Insights Agent — Project Progress Report

**Last updated:** Monday, July 14, 2026
**Project:** Oncology Care Insights Agent
**Platform:** Microsoft Foundry on Azure
**AI-103 Exam Target:** Early September 2026

---

## 🎯 Overall Project Progress

```
Week 1  ████████░░░░░░░░░░░░  40% complete
Overall ██░░░░░░░░░░░░░░░░░░  10% complete
```

---

## ✅ Completed Tasks

### Project Planning (100% done)

| Task | Date Completed |
|---|---|
| Defined project name: Oncology Care Insights Agent | Jun 28 |
| Wrote project scope doc (problem statement, cancer types, responsible AI framing, success criteria) | Jun 28 |
| Wrote project definition + one-liner for resume/LinkedIn | Jul 13 |
| Created full project folder structure (downloaded as .zip) | Jul 13 |
| System prompt written with guardrails | Jul 13 |
| Build checklist created (6 weeks + AI-103 study plan) | Jul 13 |

### Week 1 — Plan & Provision (40% done)

| Task | Date Completed |
|---|---|
| Created Azure free account | Jul 13 |
| Explored Microsoft Foundry portal (ai.azure.com) | Jul 13 |
| Created resource group `oncology-agent-rg` | Jul 14 |
| Created Foundry project `oncology-care-insights` | Jul 14 |
| Deployed chat model (gpt-5-mini) | Jul 14 |
| Deployed embedding model (text-embedding-3-small) | Jul 14 |
| Copied Project endpoint + Azure OpenAI endpoint + API key | Jul 14 |

---

## ⏳ Remaining Week 1 Tasks

| Task | Est. Time |
|---|---|
| Provision Azure AI Search | 10 min |
| Provision Azure SQL Database | 15 min |
| Create Azure Key Vault | 10 min |
| Configure managed identities/RBAC | 20 min |
| Set up budget alert in Azure Cost Management | 5 min |
| Download MITRE mCODE synthetic cancer datasets | 10 min |
| Sketch/finalize Azure SQL schema | 20 min |

**Estimated time to finish Week 1:** ~90 minutes

---

## 🔜 Upcoming Weeks

| Week | Focus | Status |
|---|---|---|
| Week 1 (Jul 8–14) | Plan & provision | 🟡 In progress |
| Week 2 (Jul 15–21) | Data pipeline & RAG corpus | 🔜 Not started |
| Week 3 (Jul 22–28) | Agent & tools | 🔜 Not started |
| Week 4 (Jul 29–Aug 4) | Front-end, safety, observability | 🔜 Not started |
| Week 5 (Aug 5–11) | Evaluation & iteration | 🔜 Not started |
| Week 6 (Aug 12–18) | Deploy, document, polish | 🔜 Not started |
| Week 7 (Aug 19–25) | AI-103 gap study: Computer Vision | 🔜 Not started |
| Week 8 (Aug 26–Sep 1) | AI-103 gap study: Text Analysis + final prep | 🔜 Not started |

---

## 🏗️ Architecture Progress

| Component | Status |
|---|---|
| Microsoft Foundry project | ✅ Live |
| gpt-5-mini (chat model) | ✅ Deployed |
| text-embedding-3-small (embedding model) | ✅ Deployed |
| Azure AI Search | ⏳ Not provisioned |
| Azure SQL Database | ⏳ Not provisioned |
| Azure Key Vault | ⏳ Not provisioned |
| Azure Functions (SQL tool) | ⏳ Not built |
| Foundry Agent | ⏳ Not built |
| Frontend chat app | ⏳ Not built |
| CI/CD pipeline (GitHub Actions + Bicep) | ⏳ Not built |

---

## 📁 Project Deliverables

| Deliverable | Status |
|---|---|
| Project folder structure | ✅ Created + downloaded |
| Scope doc (`docs/scope.md`) | ✅ Written |
| Project definition + resume one-liner | ✅ Written |
| Build checklist (`docs/checklist.md`) | ✅ Written |
| System prompt (`src/agent/system_prompt.txt`) | ✅ Written |
| Architecture doc (`docs/architecture.md`) | ✅ Template ready |
| README | ✅ Template ready |
| Azure SQL schema | ⏳ Sketched, not finalized |
| NCI PDQ guideline data | ⏳ Not downloaded |
| Synthea/mCODE patient data | ⏳ Not downloaded |
| Eval question set | ⏳ Template ready |
| Bicep IaC templates | ⏳ Skeleton only |

---

## 🎓 AI-103 Study Progress

| Domain | Coverage so far |
|---|---|
| Domain 1 — Plan & manage Azure AI solutions | 🟡 Learning by doing (provisioning) |
| Domain 2 — Generative AI & agentic solutions | ⏳ Starts Week 2 |
| Domain 3 — Computer vision | ⏳ Week 7 |
| Domain 4 — Text analysis | ⏳ Week 8 |
| Domain 5 — Information extraction | ⏳ Week 2 |

---

## 💡 Key Decisions Made

| Decision | Reason |
|---|---|
| Used gpt-5-mini instead of GPT-4o | GPT-4o deprecated for new accounts; gpt-5-mini is GA and sufficient for this project |
| Used text-embedding-3-small instead of large | Large model unavailable on free quota; small gives excellent RAG quality at lower cost |
| Cancer types: Breast, Lung, Colorectal | Synthea has dedicated modules for all three; well-covered by NCI PDQ |
| Guideline source: NCI PDQ | Public domain, peer-reviewed, organized by cancer type + stage |
| Patient data: Synthea/mCODE | Zero PHI risk; mCODE format is real-world oncology interoperability standard |

---

## 💪 What's Been Accomplished

Started with zero Azure experience and in two sessions achieved:
- A live Microsoft Foundry project with a real project endpoint
- Two deployed AI models (chat + embedding)
- A fully scaffolded codebase ready to build into
- A scope doc, system prompt, and build plan
- Full project folder structure committed to GitHub

---

## 📝 Update Log

| Date | Update |
|---|---|
| Jun 28, 2026 | Project planning complete — scope doc written |
| Jul 13, 2026 | Azure account created, Foundry portal explored, project folder created |
| Jul 14, 2026 | Resource group created, Foundry project live, gpt-5-mini + text-embedding-3-small deployed |

---

*Update this file at the end of every session to track progress.*
