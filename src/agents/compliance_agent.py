from src.core.llm import get_llm
from src.core.state import WarRoomState
from langsmith import traceable
from dotenv import load_dotenv
load_dotenv()

class ComplianceAgent:

    def __init__(self):
        self.llm = get_llm()
        
    @traceable(name="compliance_agent_checks")
    def compliance_checks(self, loan_data):
        flags = []
        veto = False

        # AML Flag
        if loan_data.aml_flag:
            flags.append("AML Red Flag")
            veto = True

        # Grey List Director
        if loan_data.director_grey_list:
            flags.append("Director on Grey List")
            veto = True

        # Offshore Deposit Check
        if loan_data.offshore_deposit > 500000:
            flags.append("Large Offshore Deposit Source of Funds Required")

        return flags, veto
    
    @traceable(name="generate_compliance_reasoning")
    def generate_reasoning(self, loan_data, flags, veto):
        prompt = f"""
You are a strict banking compliance officer.

Loan Data: {loan_data}
Compliance Flags: {flags}
Veto Triggered: {veto}

Explain regulatory concerns clearly.
If veto is triggered, justify why the loan must be blocked.
Be formal and procedural.
"""

        response = self.llm.invoke(prompt)
        return response.content
    
    @traceable(name="compliance_evaluation")
    def evaluate(self, state: WarRoomState) -> WarRoomState:
        loan_data = state["loan_data"]
        flags, veto = self.compliance_checks(loan_data)
        reasoning = self.generate_reasoning(loan_data, flags, veto)

        state["compliance_opinion"] = reasoning
        state["flags"].extend(flags)
        state["veto"] = veto
        state["turn_count"] += 1

        return state