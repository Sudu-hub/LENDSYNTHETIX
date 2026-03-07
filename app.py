import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import uuid
from src.utils.history_viewer import fetch_warroom_history

from src.core.workflow import build_graph
from src.core.checkpointer import get_checkpointer
from src.core.state import LoanData
from src.utils.audit_export import generate_decision_memo, export_memo_to_pdf

st.set_page_config(page_title="LendSynthetix War Room", layout="wide")

st.title("🏦 LendSynthetix - Digital AI War Room")

# -----------------------
# Sidebar Inputs
# -----------------------

st.sidebar.header("Loan Application Input")

industry = st.sidebar.text_input("Industry", "Technology")
revenue_growth = st.sidebar.slider("Revenue Growth (%)", -20, 100, 30)
dscr = st.sidebar.number_input("DSCR", 0.1, 5.0, 1.2)
de_ratio = st.sidebar.number_input("Debt-to-Equity", 0.0, 5.0, 2.0)
collateral = st.sidebar.number_input("Collateral Value", 0.0, 100000000.0, 0.0)
offshore = st.sidebar.number_input("Offshore Deposit", 0.0, 100000000.0, 0.0)

grey_list = st.sidebar.checkbox("Director on Grey List?")
aml_flag = st.sidebar.checkbox("AML Flag?")

stress_mode = st.sidebar.checkbox("Run Stress Test Scenario")
compare_mode = st.sidebar.checkbox("Compare Two Scenarios")

if compare_mode:

    st.sidebar.markdown("### Scenario B")

    industry_b = st.sidebar.text_input("Industry B", "Manufacturing")
    growth_b = st.sidebar.slider("Revenue Growth B (%)", -20, 100, 10)
    dscr_b = st.sidebar.number_input("DSCR B", 0.1, 5.0, 1.0)
    de_ratio_b = st.sidebar.number_input("Debt-to-Equity B", 0.0, 5.0, 3.5)

run_button = st.sidebar.button("🚀 Run War Room")


# -----------------------
# Risk Gauge
# -----------------------

def risk_gauge(score):

    score = score if score is not None else 0

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

    if stress_mode:
        revenue_growth -= 20
        dscr -= 0.3

    loan = LoanData(
        industry=industry,
        revenue_growth=revenue_growth / 100,
        dscr=dscr,
        debt_to_equity=de_ratio,
        collateral_value=collateral if collateral > 0 else None,
        offshore_deposit=offshore,
        director_grey_list=grey_list,
        aml_flag=aml_flag,
    )

    state = {
        "loan_data": loan,
        "sales_opinion": None,
        "risk_opinion": None,
        "compliance_opinion": None,
        "flags": [],
        "veto": False,
        "turn_count": 0,
        "risk_score": None,
        "final_decision": None,
        "decision_summary": None,
        "debate_round": 0,
        "max_rounds": 2,
        "consensus_reached": False,
    }

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    # -----------------------
    # Run Graph
    # -----------------------

    with get_checkpointer() as checkpointer:

        graph = build_graph(checkpointer)

        # Scenario A
        final_state = graph.invoke(state, config=config)

        result_b = None

        # Scenario B
        if compare_mode:

            loan_b = LoanData(
                industry=industry_b,
                revenue_growth=growth_b / 100,
                dscr=dscr_b,
                debt_to_equity=de_ratio_b,
                collateral_value=collateral,
                offshore_deposit=offshore,
                director_grey_list=grey_list,
                aml_flag=aml_flag,
            )

            state_b = state.copy()
            state_b["loan_data"] = loan_b

            config_b = {
                "configurable": {
                    "thread_id": str(uuid.uuid4())
                }
            }

            result_b = graph.invoke(state_b, config=config_b)

    # -----------------------
    # Decision Metrics
    # -----------------------

    st.subheader("📊 Decision Overview")

    risk_score = final_state.get("risk_score", 0)
    debate_round = final_state.get("debate_round", 0)
    turn_count = final_state.get("turn_count", 0)
    decision = final_state.get("final_decision", "UNKNOWN")

    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", risk_score)
    col2.metric("Debate Rounds", debate_round)
    col3.metric("Total Turns", turn_count)

    if "REJECT" in decision.upper():
        st.error(f"Final Decision: {decision}")
    elif "APPROVE" in decision.upper():
        st.success(f"Final Decision: {decision}")
    else:
        st.warning(f"Final Decision: {decision}")

    st.plotly_chart(risk_gauge(risk_score))

    # -----------------------
    # Agent Debate
    # -----------------------

    st.subheader("🗣 War Room Debate")

    st.markdown("### Risk Agent")
    st.write(final_state.get("risk_opinion"))

    st.markdown("### Sales Agent")
    st.write(final_state.get("sales_opinion"))

    st.markdown("### Compliance Agent")
    st.write(final_state.get("compliance_opinion"))

    # -----------------------
    # Risk Flags
    # -----------------------

    st.subheader("🚩 Risk Flags")

    flags = final_state.get("flags", [])

    if flags:

        flag_df = pd.DataFrame({"Flag": flags})
        st.dataframe(flag_df)

        counts = flag_df["Flag"].value_counts().reset_index()
        counts.columns = ["Flag", "Count"]

        fig = px.bar(counts, x="Flag", y="Count")
        st.plotly_chart(fig)

    else:
        st.success("No Risk Flags")

    # -----------------------
    # Scenario Comparison
    # -----------------------

    if compare_mode and result_b:

        comparison = pd.DataFrame({
            "Scenario": ["A", "B"],
            "Risk Score": [
                final_state.get("risk_score"),
                result_b.get("risk_score")
            ],
            "Decision": [
                final_state.get("final_decision"),
                result_b.get("final_decision")
            ]
        })

        st.subheader("⚖ Scenario Comparison")
        st.table(comparison)

    # -----------------------
    # Export Memo
    # -----------------------

    memo_text = generate_decision_memo(final_state)
    pdf_file = export_memo_to_pdf(final_state)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📄 Download PDF Memo",
            f,
            file_name="decision_memo.pdf"
        )

    st.download_button(
        "📄 Download TXT Memo",
        memo_text,
        file_name="decision_memo.txt"
    )


# -----------------------
# System Architecture
# -----------------------

with st.expander("⚙ System Architecture"):

    st.markdown("""
### LendSynthetix AI War Room Architecture

**1️⃣ Sales Agent**  
Advocates for loan approval and highlights growth potential.

**2️⃣ Risk Agent**  
Evaluates financial metrics and generates a risk score.

**3️⃣ Compliance Agent**  
Checks AML/KYC risks and can veto risky approvals.

**4️⃣ Moderator Agent**  
Aggregates agent opinions and finalizes the decision.

**5️⃣ LangGraph Debate Engine**  
Coordinates multi-round debate between agents.

**6️⃣ PostgreSQL Memory Layer**  
Stores agent decisions and workflow states.

**7️⃣ Audit Export System**  
Generates explainable decision memo (PDF/TXT).

This system simulates a **real institutional credit committee using AI agents.**
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

    except Exception as e:

        st.warning("History not available yet.")