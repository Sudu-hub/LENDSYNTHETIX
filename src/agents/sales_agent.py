from src.core.llm import get_llm
from src.core.state import WarRoomState


class SalesAgent:

    def __init__(self):
        self.llm = get_llm()

    def sales_insights(self, loan_data):
        positives = []

        if loan_data.revenue_growth > 20:
            positives.append("Strong Revenue Growth")

        if loan_data.industry in ["Tech SaaS", "AI", "FinTech"]:
            positives.append("High Growth Industry")

        if loan_data.dscr>= 1.1:
            positives.append("Acceptable DSCR with Growth Potential")

        return positives

    def generate_reasoning(self, loan_data, positives, risk_flags):
        prompt = f"""
You are a senior relationship manager in a commercial bank.

Your objective is to maximize approval while maintaining credibility.

Loan Data: {loan_data}
Positive Indicators: {positives}
Risk Flags Raised: {risk_flags}

Address each risk flag directly.
Provide counterarguments grounded in business growth, industry trends, and relationship value.
Be structured and persuasive.
"""

        response = self.llm.invoke(prompt)
        return response.content

    def evaluate(self, state: WarRoomState) -> WarRoomState:
        loan_data = state["loan_data"]
        risk_flags = state["flags"]

        positives = self.sales_insights(loan_data)
        reasoning = self.generate_reasoning(loan_data, positives, risk_flags)

        state["sales_opinion"] = reasoning
        state["turn_count"] += 1

        return state