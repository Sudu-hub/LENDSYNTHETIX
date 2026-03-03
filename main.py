from src.core.workflow import build_graph
from src.core.state import WarRoomState
from data.sample_cases import input_a

graph = build_graph()

state: WarRoomState = {
    "loan_data": input_a,
    "sales_opinion": None,
    "risk_opinion": None,
    "compliance_opinion": None,
    "flags": [],
    "veto": False,
    "turn_count": 0,
    "risk_score": None,
    "final_decision": None,
    "decision_summary": None,
    "debate_round": 0,
    "max_rounds": 2,
    "consensus_reached": False,
}

result = graph.invoke(state)

print("\nFINAL DECISION:", result["final_decision"])
print("\nSUMMARY:\n", result["decision_summary"])
print("\nTURNS:", result["turn_count"])