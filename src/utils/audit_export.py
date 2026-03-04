import os
from datetime import datetime
from src.core.state import WarRoomState


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


def export_memo_to_txt(state: WarRoomState, folder="outputs"):

    os.makedirs(folder, exist_ok=True)

    memo_text = generate_decision_memo(state)

    filename = f"{folder}/decision_memo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(memo_text)

    return filename