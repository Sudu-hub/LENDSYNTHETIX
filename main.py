from src.agents.risk_agent import RiskAgent
from src.agents.compliance_agent import ComplianceAgent
from data.sample_cases import input_b
from src.core.state import WarRoomState

state: WarRoomState = {
    "loan_data": input_b,
    "sales_opinion": "",
    "risk_opinion": "",
    "compliance_opinion": "",
    "flags": [],
    "veto": False,
    "turn_count": 0,
    "final_decision": "",
    "risk_score": 0,
}

risk = RiskAgent()
compliance = ComplianceAgent()

state = risk.evaluate(state)
state = compliance.evaluate(state)

if state["veto"]:
    state["final_decision"] = "REJECTED Compliance Veto"
else:
    if state["risk_score"] < 60:
        state["final_decision"] = "REJECTED High Risk"
    else:
        state["final_decision"] = "APPROVED"

print("FLAGS:", state["flags"])
print("VETO:", state["veto"])
print("RISK SCORE:", state["risk_score"])
print("\nCOMPLIANCE OPINION:\n", state["compliance_opinion"])
print("\nFINAL DECISION:", state["final_decision"])