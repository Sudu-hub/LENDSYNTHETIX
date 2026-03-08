import yaml
from langsmith import traceable
from src.core.llm import get_llm
from src.core.state import WarRoomState
from dotenv import load_dotenv
load_dotenv()


class RiskAgent:

    def __init__(self):
        self.llm = get_llm()
        with open("config/risk_thresholds.yaml", "r") as f:
            self.thresholds = yaml.safe_load(f)

    @traceable(name="deterministic_risk_checks")
    def deterministic_checks(self, loan_data):
        flags = []

        if loan_data.dscr < self.thresholds["min_dscr"]:
            flags.append("Low DSCR")

        if loan_data.debt_to_equity > self.thresholds["max_debt_to_equity"]:
            flags.append("High Debt-to-Equity")

        if loan_data.revenue_growth < self.thresholds["min_revenue_growth"]:
            flags.append("Low Revenue Growth")

        if loan_data.collateral_value == 0:
            flags.append("No Collateral")

        return flags

    @traceable(name="risk_score_calculation")
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

    @traceable(name="risk_reasoning_llm")
    def generate_reasoning(self, loan_data, flags):

        prompt = f"""
You are a SENIOR CREDIT UNDERWRITER responsible for protecting the bank's capital.

You are skeptical and analytical.

Loan Data:
{loan_data}

Risk Flags Identified:
{flags}

Evaluate the borrower using:

1. Debt Service Coverage Ratio (DSCR)
2. Collateral Quality
3. Cash Flow Stability
4. Revenue Growth
5. Leverage Risk

Provide a structured credit memo with:

- Key Risk Observations
- Strengths
- Weaknesses
- Final Risk Opinion
"""

        response = self.llm.invoke(prompt)

        return response.content


    @traceable(name="risk_agent_evaluation")
    def evaluate(self, state: WarRoomState) -> WarRoomState:

        loan_data = state["loan_data"]

        flags = self.deterministic_checks(loan_data)
        risk_score = self.calculate_risk_score(flags)
        reasoning = self.generate_reasoning(loan_data, flags)

        state["risk_opinion"] = reasoning
        state["risk_score"] = risk_score
        if "flags" not in state:
            state["flags"] = []
        state["flags"].extend(flags)
        state["turn_count"] += 1

        # Increment debate round here
        state["debate_round"] += 1

        return state