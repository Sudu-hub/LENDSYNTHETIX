import streamlit as st
from src.core.workflow import build_graph
from src.core.state import LoanData
from src.utils.metrics import calculate_metrics
from src.utils.audit_export import export_memo_to_txt

st.set_page_config(page_title="LendSynthetix War Room", layout="wide")

st.title("LendSynthetix-Digital War Room")

# -----------------------
# Loan Input Form
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

run_button = st.sidebar.button("Run War Room")


# -----------------------
# Run Engine
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
    final_state = graph.invoke(state)

    metrics = calculate_metrics(final_state)

    # -----------------------
    # Results Display
    # -----------------------

    st.subheader("Decision Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", final_state["risk_score"])
    col2.metric("Debate Rounds", final_state["debate_round"])
    col3.metric("Total Turns", final_state["turn_count"])

    st.success(f"Final Decision: {final_state['final_decision']}")

    st.subheader("Agent Opinions")

    st.markdown("**Sales:**")
    st.write(final_state["sales_opinion"])

    st.markdown("**Risk:**")
    st.write(final_state["risk_opinion"])

    st.markdown("**Compliance:**")
    st.write(final_state["compliance_opinion"])

    st.subheader("Executive Summary")
    st.write(final_state["decision_summary"])

    file_path = export_memo_to_txt(final_state)
    st.info(f"Audit memo saved at: {file_path}")