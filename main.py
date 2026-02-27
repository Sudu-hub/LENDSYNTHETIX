from src.agents.risk_agent import RiskAgent
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
updated_state = risk.evaluate(state)

print("FLAGS:", updated_state["flags"])
print("RISK SCORE:", updated_state["risk_score"])
print("RISK OPINION:\n", updated_state["risk_opinion"])