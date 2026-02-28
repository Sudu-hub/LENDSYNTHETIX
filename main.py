from src.agents.risk_agent import RiskAgent
from src.agents.sales_agent import SalesAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.moderator_agent import ModeratorAgent
from data.sample_cases import input_a
from src.core.state import WarRoomState

state: WarRoomState = {
    "loan_data": input_a,
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
sales = SalesAgent()
compliance = ComplianceAgent()
moderator = ModeratorAgent()

state = risk.evaluate(state)
state = sales.evaluate(state)
state = compliance.evaluate(state)
state = moderator.decide(state)

print("\nFLAGS:", state["flags"])
print("RISK SCORE:", state["risk_score"])
print("VETO:", state["veto"])
print("FINAL DECISION:", state["final_decision"])
print("TURNS:", state["turn_count"])