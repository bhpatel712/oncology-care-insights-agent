# Oncology Care Insights Agent — Build & Study Checklist

**Project:** Agent-based RAG application on Microsoft Foundry for oncology decision support (breast, lung, colorectal cancer)
**Timeline:** July 1 – August 29, 2026
**Exam target:** AI-103 — early September 2026
**Goal:** Portfolio-ready agent app + AI-103 certification

---

## ✅ Completed before July 1st

- [x] **Jun 28** — Wrote one-page project scope doc (problem statement, 3 cancer types, responsible-AI framing, success criteria)

---

## Prerequisites (complete before or during Week 1)

- [ ] Azure subscription set up (pay-as-you-go, free trial credits applied if available)
- [ ] GitHub account ready — new repo created for this project
- [ ] Python 3.10+ installed locally
- [ ] VS Code installed with Python + Azure extensions
- [ ] Azure CLI (`az`) and/or Azure Developer CLI (`azd`) installed
- [ ] Java JDK installed (only if generating your own Synthea data — skip if using MITRE's pre-built mCODE datasets)

---

## Week 1: July 1 – July 7 — Plan & provision

> **AI-103 study focus this week:** Domain 1 — Foundry project structure, managed identity vs. API keys, resource tiers, PTU vs. pay-as-you-go cost planning. Study what you're actively provisioning each day.

### Carry-over from June 28–30
- [ ] Confirm Azure subscription/billing is active and ready to use
- [ ] Explore the Microsoft Foundry portal — get familiar with the layout before building
- [ ] Create a resource group for the project
- [ ] Create a Microsoft Foundry project inside the resource group
- [ ] Deploy a chat model (GPT-4o or GPT-4.1)
- [ ] Deploy an embedding model (text-embedding-3-large)

### July 1 (Tue)
- [ ] Provision Azure AI Search (Free tier to start — 50MB, 3 indexes)
- [ ] Provision Azure SQL Database (Basic DTU tier, ~$4.90/month)
- [ ] Create Azure Key Vault

### July 2 (Wed)
- [ ] Configure managed identities/RBAC across all provisioned services (Foundry → Search, Function → SQL, etc.)
- [ ] Set up a budget alert in Azure Cost Management (notify at $30 threshold)

### July 3 (Thu)
- [ ] Download MITRE's pre-built mCODE synthetic cancer datasets (or set up Synthea's cancer modules)
- [ ] Review the raw data — understand what fields are available for breast, lung, colorectal cancer

### July 4 (Fri) — Light day
- [ ] Sketch the Azure SQL schema on paper or in a doc (Patients, Diagnoses/Staging, Treatments, Observations)
- [ ] Commit scope doc + schema sketch to GitHub repo

### July 5 (Sat)
- [ ] AI-103 study session: Domain 1 practice questions — cost planning, managed identity scenarios, resource tier trade-offs

**Deliverable:** Working Azure environment — Foundry project + models live, Search and SQL provisioned, raw oncology data in hand, budget alert set.
**AI-103 domain covered:** Domain 1 — Plan and manage Azure AI solutions (25–30%)

---

## Week 2: July 8 – July 14 — Data pipeline & RAG corpus

> **AI-103 study focus this week:** Domain 2 (RAG half) + Domain 5 (Information extraction) — vector vs. hybrid search, chunking strategy, grounding, embeddings. Read while you build.

### July 8 (Tue)
- [ ] Start Python ETL: parse Synthea/mCODE FHIR bundles or CSV files into normalized tables
- [ ] Create Azure SQL tables from your schema

### July 9 (Wed)
- [ ] Finish loading data into Azure SQL
- [ ] Validate with cohort-count queries (e.g., how many breast cancer patients, by stage)

### July 10 (Thu)
- [ ] Pull NCI PDQ health-professional summaries for breast cancer from cancer.gov (treatment, staging, prognosis)
- [ ] Pull PDQ summaries for lung cancer

### July 11 (Fri)
- [ ] Pull PDQ summaries for colorectal cancer
- [ ] Clean and tag all PDQ content with metadata (cancer_type, stage, section, source_url)

### July 12 (Sat)
- [ ] Write the chunking script (~500–800 token chunks with overlap)
- [ ] Generate embeddings for all chunks

### July 13 (Sun)
- [ ] Push embedded chunks into Azure AI Search
- [ ] Configure vector + semantic hybrid search with metadata filters by cancer_type and stage

### July 14 (Mon)
- [ ] Manually test retrieval against ~15 sample questions per cancer type
- [ ] Tune chunking or index config if results are weak
- [ ] AI-103 study session: Domain 2 RAG concepts + Domain 5 practice questions

**Deliverable:** Azure SQL populated with the oncology cohort; Azure AI Search returning well-grounded guideline passages.
**AI-103 domains covered:** Domain 2 (RAG half, 30–35%) + Domain 5 — Information extraction (10–15%)

---

## Week 3: July 15 – July 21 — Agent & tools

> **AI-103 study focus this week:** Domain 2 (agentic half) — the biggest single domain on the exam. Study agent orchestration, tool-calling patterns, multi-agent concepts in parallel with your build.

### July 15 (Tue)
- [ ] Set up Foundry Agent Service
- [ ] Write the base system prompt (scope, tone, decision-support guardrail, synthetic-data disclaimer)

### July 16 (Wed)
- [ ] Wire Azure AI Search as the agent's retrieval tool
- [ ] Test plain RAG questions through the agent — confirm grounded answers with citations

### July 17 (Thu)
- [ ] Build the Azure Function wrapping parameterized SQL queries
  - `get_cohort_stats(cancer_type, stage)`
  - `get_patient_panel_summary(cancer_type)`
  - `get_treatment_distribution(cancer_type)`

### July 18 (Fri)
- [ ] Secure the Azure Function to Azure SQL via managed identity
- [ ] Register the SQL function as a tool on the agent

### July 19 (Sat)
- [ ] Write clear tool descriptions and parameter schemas so the model reliably calls the right tool
- [ ] Test multi-tool questions that need both retrieval and SQL together

### July 20 (Sun)
- [ ] Stress-test edge cases — ambiguous asks, out-of-scope requests (PHI, diagnosis questions)
- [ ] Confirm guardrails hold consistently

### July 21 (Mon)
- [ ] Fix any guardrail gaps or tool-routing failures found during testing
- [ ] AI-103 study session: Domain 2 agentic concepts + practice questions

**Deliverable:** A working agent that correctly chooses between and combines tools, with guardrails holding under pressure.
**AI-103 domain covered:** Domain 2 — Generative AI and agentic solutions, agentic half (30–35%)

---

## Week 4: July 22 – July 28 — Front-end, safety & observability

> **AI-103 study focus this week:** Domain 1 continued — responsible AI configuration, content filter severity thresholds, monitoring with Log Analytics and Application Insights. Directly reinforced by your safety and tracing work this week.

### July 22 (Tue)
- [ ] Scaffold the chat front-end (Streamlit for speed, or React + Vite for a more polished look)

### July 23 (Wed)
- [ ] Wire the front-end to the agent via the `azure-ai-projects` SDK (2.0.0+)

### July 24 (Thu)
- [ ] Add citation display — show which guideline passage was retrieved and which tool(s) fired per answer

### July 25 (Fri)
- [ ] Turn on Content Safety filters
- [ ] Add a visible "Synthetic data — decision support only, not a clinical tool" banner to the UI

### July 26 (Sat)
- [ ] Wire Application Insights / Foundry tracing for tokens, latency, and tool-call logs

### July 27 (Sun)
- [ ] Polish UI — loading states, error handling for tool failures, clean layout

### July 28 (Mon)
- [ ] Full end-to-end walkthrough; document rough edges for next week's eval
- [ ] AI-103 study session: Domain 1 responsible AI + monitoring practice questions

**Deliverable:** A usable, cited, safety-filtered chat app with visible tracing and a clean UI.
**AI-103 domain covered:** Domain 1 — Plan and manage Azure AI solutions, safety/observability sub-topics (25–30%)

---

## Week 5: July 29 – August 4 — Evaluation & iteration

> **AI-103 study focus this week:** Domain 2 evaluation sub-topics — groundedness, relevance, safety scoring. Same work as your project, dual purpose. Also: run your first full practice exam.

### July 29 (Tue)
- [ ] Draft the eval question set — RAG-only, SQL-only, combined, adversarial categories

### July 30 (Wed)
- [ ] Finish the eval set (target 30–50 questions total)

### July 31 (Thu)
- [ ] Run Foundry's evaluation SDK for groundedness, relevance, coherence, and safety

### August 1 (Fri)
- [ ] Evaluate tool-call accuracy on the combined-agent questions

### August 2 (Sat)
- [ ] Diagnose top failure patterns (chunking gaps, vague tool descriptions, missing guardrails)
- [ ] Fix the top issues found

### August 3 (Sun)
- [ ] Re-run the full eval set after fixes
- [ ] Document before/after improvement clearly

### August 4 (Mon)
- [ ] Write up eval methodology and results section for the README
- [ ] AI-103 study session: First full timed practice exam (40–60 questions) — review by domain

**Deliverable:** Documented eval results showing measurable improvement — a strong portfolio and interview talking point.
**AI-103 domain covered:** Domain 2 — Evaluation and responsible AI sub-topics (30–35%)

---

## Week 6: August 5 – August 11 — Deploy, document & polish

> **AI-103 study focus this week:** Domain 1 CI/CD and IaC patterns — directly reinforced by your Bicep + GitHub Actions work.

### August 5 (Tue)
- [ ] Start Bicep templates for every resource (resource group, Foundry, Search, SQL, Key Vault, Functions)

### August 6 (Wed)
- [ ] Finish Bicep; test a clean deploy from scratch on a fresh resource group

### August 7 (Thu)
- [ ] Set up GitHub Actions pipeline to deploy infra + app code end-to-end

### August 8 (Fri)
- [ ] Write the README — architecture diagram, setup steps, screenshots, known data limitations

### August 9 (Sat)
- [ ] Record a 2–3 minute demo video or animated GIF walkthrough

### August 10 (Sun)
- [ ] Write the case-study post (problem, architecture, trade-offs, AI-103 skill mapping)

### August 11 (Mon)
- [ ] Final review — scale down/tear down idle resources, check actual cost in Azure Cost Management
- [ ] AI-103 study session: Domain 1 IaC/CI/CD practice questions + second full timed practice exam

**Deliverable:** A fully documented, deployable, portfolio-ready project with a recorded demo and case-study post.
**AI-103 domain covered:** Domain 1 — Deployment, IaC, CI/CD sub-topics (25–30%)

---

## Week 7: August 12 – August 18 — AI-103 gap study: Computer Vision

> Your project doesn't touch this domain — dedicated study week.

- [ ] Read Domain 3 Microsoft Learn modules: multimodal models for visual understanding, video analysis workflows
- [ ] Complete one hands-on lab: feed a scanned chart or medical image to GPT-4o via Content Understanding
- [ ] Study image analysis, object detection, and OCR patterns in Foundry context
- [ ] Run a 20-question practice drill on computer vision scenarios
- [ ] Review wrong answers and re-read related docs

**AI-103 domain covered:** Domain 3 — Computer vision (10–15%)

---

## Week 8: August 19 – August 25 — AI-103 gap study: Text Analysis + Final prep

> Finish the last domain, then consolidate everything before scheduling.

- [ ] Read Domain 4 Microsoft Learn modules: LLM-first entity extraction, sentiment analysis, summarization, intent routing via Azure Language in Foundry Tools
- [ ] Complete one hands-on lab: run entity extraction and summarization on a sample NCI PDQ document
- [ ] Run a 20-question practice drill on text analysis scenarios
- [ ] Run a third full timed practice exam across all 5 domains
- [ ] Identify weak domains from practice score breakdown — do a focused re-read of those sections
- [ ] Re-skim your project's architecture, eval results, and Bicep — expect scenario questions drawn from exactly this kind of real build
- [ ] Schedule the AI-103 exam for early September via Pearson VUE

**AI-103 domains covered:** Domain 4 — Text analysis (10–15%) + full consolidation

---

## After August 25 — Exam week prep

- [ ] Do a 30-minute domain-by-domain review using your notes
- [ ] Skim Microsoft's official AI-103 study guide one final time for any terminology updates
- [ ] Confirm exam appointment, ID requirements, and login details with Pearson VUE
- [ ] Take the exam — target early September

---

## Known scope limitations to disclose in your README

- Synthetic data only (Synthea/mCODE) — not validated for clinical decision-making
- Synthea's breast cancer module does not capture full pathologic staging, genomics, or metastasis detail
- This tool is decision support for clinical-ops/analyst use — not a substitute for oncologist or tumor-board judgment
- Computer vision and text analysis were studied separately, not built into this project
