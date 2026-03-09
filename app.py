import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import uuid
import os
from src.utils.history_viewer import fetch_warroom_history
from src.core.workflow import build_graph
from src.core.checkpointer import get_checkpointer
from src.utils.audit_export import generate_decision_memo, export_memo_to_pdf

# -----------------------
# Page Setup
# -----------------------

st.set_page_config(page_title="LendSynthetix War Room", layout="wide")

st.title("🏦 LendSynthetix - Digital AI Credit War Room")

# -----------------------
# Sidebar
# -----------------------

st.sidebar.header("Loan Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload Loan PDF",
    type=["pdf"]
)

run_button = st.sidebar.button("🚀 Run War Room")

# -----------------------
# Save Uploaded PDF
# -----------------------

pdf_path = None

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    pdf_path = f"uploads/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.sidebar.success("PDF uploaded successfully")

# -----------------------
# Risk Gauge
# -----------------------

def risk_gauge(score):

    score = score if score else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"},
            ],
        }
    ))

    return fig

# -----------------------
# Run War Room
# -----------------------

if run_button:

    if not pdf_path:
        st.error("Please upload a loan PDF first.")
        st.stop()

    state = {

        "pdf_path": pdf_path,

        "loan_data": None,

        "sales_opinion": None,
        "risk_opinion": None,
        "compliance_opinion": None,

        "flags": [],
        "veto": False,

        "turn_count": 0,
        "debate_round": 0,
        "max_rounds": 2,
        "consensus_reached": False,

        "risk_score": None,

        "final_decision": None,
        "decision_summary": None,
    }

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    # -----------------------
    # Run LangGraph
    # -----------------------

    with get_checkpointer() as checkpointer:

        graph = build_graph(checkpointer)

        final_state = graph.invoke(state, config=config)

    # -----------------------
    # Decision Overview
    # -----------------------

    st.subheader("📊 Decision Overview")

    risk_score = final_state.get("risk_score", 0)
    decision = final_state.get("final_decision", "review")

    col1, col2 = st.columns(2)

    col1.metric("Risk Score", risk_score)

    if decision == "approve":
        col2.success("APPROVED")
    elif decision == "reject":
        col2.error("REJECTED")
    else:
        col2.warning("REVIEW REQUIRED")

    st.plotly_chart(risk_gauge(risk_score))

    # -----------------------
    # Extracted Financial Data
    # -----------------------

    if final_state.get("loan_data"):

        st.subheader("📑 Extracted Financial Metrics")

        loan_data = final_state["loan_data"]

        data = loan_data.model_dump()

        # Convert revenue growth to %
        if "revenue_growth" in data:
            data["revenue_growth"] = f"{data['revenue_growth']*100:.1f}%"

        metrics_df = pd.DataFrame({
            "Metric": data.keys(),
            "Value": [str(v) for v in data.values()]
        })

        st.table(metrics_df)

    # -----------------------
    # Agent Debate
    # -----------------------

    st.subheader("🗣 Agent Debate")

    st.markdown("### ⚠ Risk Agent")
    st.write(final_state.get("risk_opinion"))

    st.markdown("### 📈 Sales Agent")
    st.write(final_state.get("sales_opinion"))

    st.markdown("### 🛡 Compliance Agent")
    st.write(final_state.get("compliance_opinion"))

    # -----------------------
    # Flags
    # -----------------------

    flags = final_state.get("flags", [])

    if flags:

        st.subheader("🚩 Risk Flags")

        flag_df = pd.DataFrame({"Flags": flags})

        st.table(flag_df)

    else:

        st.success("No risk flags detected")

    # -----------------------
    # Export Decision Memo
    # -----------------------

    st.subheader("📄 Export Decision")

    memo_text = generate_decision_memo(final_state)

    pdf_file = export_memo_to_pdf(final_state)

    with open(pdf_file, "rb") as f:

        st.download_button(
            "Download Decision Memo (PDF)",
            f,
            file_name="decision_memo.pdf"
        )

    st.download_button(
        "Download Decision Memo (TXT)",
        memo_text,
        file_name="decision_memo.txt"
    )


# -----------------------
# System Architecture
# -----------------------

with st.expander("⚙ System Architecture"):

    st.markdown("""
### LendSynthetix AI War Room Architecture

**1️⃣ Document Processing Layer**  
Parses messy financial PDFs and extracts financial metrics.

**2️⃣ Risk Agent**  
Analyzes DSCR, leverage, and financial stability.

**3️⃣ Sales Agent**  
Advocates for loan approval and growth potential.

**4️⃣ Compliance Agent**  
Checks AML/KYC risk and regulatory issues.

**5️⃣ Moderator Agent**  
Aggregates debate and finalizes decision.

**6️⃣ LangGraph Debate Engine**  
Coordinates multi-round AI credit committee debate.

**7️⃣ Audit Export System**  
Generates explainable credit decision memo.
""")


# -----------------------
# War Room History
# -----------------------

with st.expander("📚 War Room History (Previous Decisions)"):

    try:

        history_df = fetch_warroom_history()

        if history_df.empty:
            st.info("No previous runs found.")

        else:
            st.dataframe(history_df)

    except Exception:

        st.warning("History not available yet.")