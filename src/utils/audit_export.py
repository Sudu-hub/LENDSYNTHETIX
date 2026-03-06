import os
from datetime import datetime
from src.core.state import WarRoomState
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph


def generate_decision_memo(state: WarRoomState) -> str:

    loan = state["loan_data"]

    memo = f"""
===============================
        LendSynthetix
     Digital War Room Memo
===============================

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

--------------------------------
LOAN SUMMARY
--------------------------------
Industry: {loan.industry}
Revenue Growth: {loan.revenue_growth * 100:.2f}%
DSCR: {loan.dscr}
Debt-to-Equity: {loan.debt_to_equity}
Collateral Value: {loan.collateral_value}
Offshore Deposit: {loan.offshore_deposit}

--------------------------------
AGENT OPINIONS
--------------------------------

Sales Opinion:
{state["sales_opinion"]}

Risk Opinion:
{state["risk_opinion"]}

Compliance Opinion:
{state["compliance_opinion"]}

--------------------------------
RISK FLAGS
--------------------------------
{state["flags"]}

Risk Score: {state["risk_score"]}
Compliance Veto: {state["veto"]}

Debate Rounds: {state["debate_round"]}
Total Turns: {state["turn_count"]}

--------------------------------
FINAL DECISION
--------------------------------
{state["final_decision"]}

--------------------------------
EXECUTIVE SUMMARY
--------------------------------
{state["decision_summary"]}

===============================
END OF MEMO
===============================
"""

    return memo


def export_memo_to_pdf(state, filename="decision_memo.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    memo_text = generate_decision_memo(state)

    for line in memo_text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)

    return filename