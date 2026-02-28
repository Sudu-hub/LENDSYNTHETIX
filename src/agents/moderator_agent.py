from src.core.llm import get_llm
from src.core.state import WarRoomState


class ModeratorAgent:

    def __init__(self):
        self.llm = get_llm()

    def generate_summary(self, state: WarRoomState) -> str:
        prompt = f"""
You are the credit committee chair.

Sales Opinion:
{state["sales_opinion"]}

Risk Opinion:
{state["risk_opinion"]}

Compliance Opinion:
{state["compliance_opinion"]}

Final Decision:
{state["final_decision"]}

Write a clear executive summary explaining why this decision was made.
Be formal, structured, and audit-ready.
"""
        response = self.llm.invoke(prompt)
        return response.content

    def decide(self, state: WarRoomState) -> WarRoomState:

        # Rule 1: Compliance Veto
        if state["veto"]:
            state["final_decision"] = "REJECTED - Compliance Veto"
            state["turn_count"] += 1

            summary = self.generate_summary(state)
            state["decision_summary"] = summary
            return state

        risk_score = state["risk_score"]
        revenue_growth = state["loan_data"].revenue_growth

        # Rule 2: Risk-based decision
        if risk_score < 60:
            decision = "REJECTED - High Risk"

        elif 60 <= risk_score <= 75:
            if revenue_growth > 25:
                decision = "APPROVED WITH CONDITIONS - Growth Offset"
            else:
                decision = "ESCALATE - Committee Review Required"

        else:
            decision = "APPROVED"

        state["final_decision"] = decision
        state["turn_count"] += 1

        # Generate audit summary
        summary = self.generate_summary(state)
        state["decision_summary"] = summary

        return state