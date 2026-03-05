import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.core.workflow import build_graph
from src.core.state import LoanData
from src.utils.metrics import calculate_metrics
from src.utils.audit_export import generate_decision_memo
from src.utils.audit_export import export_memo_to_pdf

st.set_page_config(page_title="LendSynthetix War Room", layout="wide")

st.title("🏦 LendSynthetix – Digital AI War Room")

# -----------------------
# Sidebar Input
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

run_button = st.sidebar.button("🚀 Run War Room")

# -----------------------
# Risk Gauge
# -----------------------

def risk_gauge(score):
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
# Run Engine (INVOKE ONLY)
# -----------------------

if run_button:

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

    graph = build_graph()

    with st.spinner("⚙ Running AI War Room..."):
        try:
            final_state = graph.invoke(state)
        except Exception as e:
            st.error(f"System Error: {e}")
            st.stop()

    # -----------------------
    # Decision Overview
    # -----------------------

    st.subheader("📊 Decision Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", final_state.get("risk_score", "N/A"))
    col2.metric("Debate Rounds", final_state.get("debate_round", "N/A"))
    col3.metric("Total Turns", final_state.get("turn_count", "N/A"))

    decision = final_state.get("final_decision", "No Decision")

    if "REJECT" in decision.upper():
        st.error(f"Final Decision: {decision}")
    elif "APPROVE" in decision.upper():
        st.success(f"Final Decision: {decision}")
    else:
        st.warning(f"Final Decision: {decision}")

    # Risk Gauge
    if final_state.get("risk_score") is not None:
        st.plotly_chart(risk_gauge(final_state["risk_score"]))

    # -----------------------
    # Debate Timeline (Visual Impact)
    # -----------------------

    st.subheader("🕒 Debate Timeline")

    timeline_data = [
        {"Step": "Risk Review", "Order": 1},
        {"Step": "Sales Counter", "Order": 2},
        {"Step": "Compliance Check", "Order": 3},
        {"Step": "Moderator Decision", "Order": 4},
    ]

    df_timeline = pd.DataFrame(timeline_data)
    fig = px.line(df_timeline, x="Order", y="Order", text="Step")
    st.plotly_chart(fig)

    # -----------------------
    # Agent Debate View
    # -----------------------

    st.subheader("🗣 War Room Debate")

    st.markdown("### 🔍 Risk Agent")
    st.write(final_state.get("risk_opinion", "N/A"))

    st.markdown("### 💼 Sales Agent")
    st.write(final_state.get("sales_opinion", "N/A"))

    st.markdown("### 🛡 Compliance Officer")
    st.write(final_state.get("compliance_opinion", "N/A"))

    # -----------------------
    # Executive Summary
    # -----------------------

    st.subheader("📝 Executive Summary")
    st.write(final_state.get("decision_summary", "No summary generated."))

    # -----------------------
    # Performance Analytics
    # -----------------------

    st.subheader("📈 Performance Analytics")

    metrics_df = pd.DataFrame({
        "Metric": [
            "Risk Score",
            "Debate Rounds",
            "Turn Count",
            "Total Flags"
        ],
        "Value": [
            final_state.get("risk_score", 0),
            final_state.get("debate_round", 0),
            final_state.get("turn_count", 0),
            len(final_state.get("flags", []))
        ]
    })

    fig = px.bar(metrics_df, x="Metric", y="Value")
    st.plotly_chart(fig)

    # -----------------------
    # Download Memo
    # -----------------------

    memo_text = generate_decision_memo(final_state)
    
    pdf_file_path = export_memo_to_pdf(final_state)

    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Decision Memo (PDF)",
            data=pdf_file,
            file_name="decision_memo.pdf",
            mime="application/pdf"
        )
    

    st.download_button(
        label="📄 Download Decision Memo",
        data=memo_text,
        file_name="decision_memo.txt",
        mime="text/plain"
    )