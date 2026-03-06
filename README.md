# LendSynthetix – AI Digital War Room for Lending Decisions

## Problem

Commercial lending decisions are slow and fragmented.
Sales teams push for approvals, Risk teams focus on exposure, and Compliance checks for regulatory violations.

These decisions can take **days or weeks**.

## Solution

LendSynthetix simulates a **digital credit committee** using **AI agents that debate a loan application** before making a final lending decision.

The system evaluates:

• Financial risk
• Growth potential
• Compliance violations

and produces a **transparent, explainable lending decision in seconds**.

---

## Architecture

The system uses **LangGraph** to orchestrate four AI agents:

**Sales Agent**

* Advocates for loan approval
* Highlights growth opportunity

**Risk Agent**

* Evaluates credit risk
* Generates risk score
* Flags financial concerns

**Compliance Agent**

* Performs AML / KYC checks
* Can veto risky approvals

**Moderator Agent**

* Aggregates opinions
* Produces final decision

---

## Features

• Multi-Agent AI Debate
• Financial Risk Scoring
• Compliance Veto System
• Explainable Decision Logs
• Scenario Comparison Mode
• Risk Flag Analytics
• Stress Test Simulation
• Executive Dashboard
• PDF + TXT Audit Memo

---

## Tech Stack

Python
Streamlit
LangGraph
OpenRouter LLM API
Plotly
Pydantic

---

## How to Run

Install dependencies:

```
pip install -r requirements.txt
```

Run the dashboard:

```
streamlit run app.py
```

---

## Demo

The dashboard allows users to:

1️⃣ Enter loan details
2️⃣ Watch AI agents debate
3️⃣ See risk analysis
4️⃣ Generate an audit memo

---

## Why This Matters

LendSynthetix demonstrates how **AI agent collaboration can simulate institutional decision-making**, reducing lending decision time from **days to seconds**.

---

## Authors

Built for the **AI/ML Data Buildathon by vConstruct**.
