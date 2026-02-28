import yaml
from src.core.llm import get_llm
from src.core.state import WarRoomState


class RiskAgent:

    def __init__(self):
        self.llm = get_llm()
        with open("config/risk_thresholds.yaml", "r") as f:
            self.thresholds = yaml.safe_load(f)

    def deterministic_checks(self, loan_data):
        flags = []

        if loan_data.dscr < self.thresholds["min_dscr"]:
            flags.append("Low DSCR")

        if loan_data.debt_to_equity> self.thresholds["max_debt_to_equity"]:
            flags.append("High Debt-to-Equity")

        if loan_data.revenue_growth < self.thresholds["min_revenue_growth"]:
            flags.append("Low Revenue Growth")

        if loan_data.collateral_value == 0:
            flags.append("No Collateral")

        return flags

    def calculate_risk_score(self, flags):
        score = 100

        for flag in flags:
            if flag == "Low DSCR":
                score -= 30
            elif flag == "High Debt-to-Equity":
                score -= 25
            elif flag == "No Collateral":
                score -= 20
            elif flag == "Low Revenue Growth":
                score -= 15

        return max(score, 0)

    def generate_reasoning(self, loan_data, flags):
        prompt = f"""
You are a senior credit underwriter.
Loan Data: {loan_data}
Risk Flags Identified: {flags}

Explain clearly why this loan is risky or acceptable.
Be structured and professional.
"""
        response = self.llm.invoke(prompt)
        return response.content

    def evaluate(self, state: WarRoomState) -> WarRoomState:
        loan_data = state["loan_data"]

        flags = self.deterministic_checks(loan_data)
        risk_score = self.calculate_risk_score(flags)
        reasoning = self.generate_reasoning(loan_data, flags)

        state["risk_opinion"] = reasoning
        state["risk_score"] = risk_score
        state["flags"].extend(flags)
        state["turn_count"] += 1

        return state