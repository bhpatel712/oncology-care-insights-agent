# Project Scope: Oncology Care Insights Agent

**Status:** Final · v1.0 · June 28, 2026

## Problem Statement

Clinical operations and care management teams need fast, defensible answers that combine two things that normally live in separate systems: what authoritative oncology guidance recommends for a given cancer type and stage, and how their own patient population compares against that guidance. Today, answering a question like *"How many of our breast cancer patients are following the NCI-recommended treatment pathway for their stage?"* requires manually cross-referencing static guideline documents against ad hoc SQL queries — slow, inconsistent, and hard to audit.

This project builds an agent-based AI application that answers these questions directly. A clinical-ops analyst asks a question in plain language, and the agent decides whether to retrieve grounded guideline content, query the synthetic patient population, or combine both — returning a cited, auditable answer.

## Scope: Cancer Types

The project covers three cancer types, chosen because each has a dedicated Synthea synthetic-patient module and well-structured NCI PDQ treatment guidance:

- Breast cancer
- Lung cancer
- Colorectal cancer

**Explicitly out of scope for this version:** other cancer types, real patient data of any kind, and genomic/biomarker-level precision beyond what the synthetic data actually supports.

## Responsible AI Framing

This is a decision-support tool for clinical operations and data analysts — not a clinical or diagnostic tool, and not a substitute for an oncologist or tumor board.

- All patient data is synthetic (Synthea / mCODE format) — zero real PHI, ever.
- The agent will not answer questions framed as diagnosing or treating a specific real patient.
- Every answer must cite its source — the guideline document it retrieved from, the cohort query it ran, or both.
- Known data limitations (e.g., Synthea's breast cancer module not capturing full pathologic staging or genomics) are documented openly, not hidden.

## Success Criteria

The project is considered successful if:

1. The agent correctly distinguishes between RAG-only, SQL-only, and combined questions, and calls the right tool(s) on at least ~90% of a held-out evaluation set (30–50 questions).
2. Evaluation scores for groundedness and relevance (via Foundry's evaluation tooling) show measurable improvement between the first and final iteration.
3. The agent reliably declines out-of-scope or unsafe requests (e.g., real-patient diagnosis questions) without exception on the adversarial eval subset.
4. The full stack (Foundry Agent Service, Azure AI Search, Azure SQL, front-end) deploys cleanly from Bicep/IaC on a fresh resource group.
5. The finished project is documented well enough — README, architecture diagram, demo recording — to stand alone as a portfolio piece and a concrete talking point in interviews.
