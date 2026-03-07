from src.core.workflow import build_graph
from src.core.state import WarRoomState
from src.utils.audit_export import export_memo_to_pdf
from src.utils.metrics import calculate_metrics
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
final_state = graph.invoke(state)

for message_chunk, metadata in graph.stream(state, stream_mode="messages"): #Streaming
    if message_chunk.content:
        print(message_chunk.content, end="", flush=True)
        
file_path = export_memo_to_pdf(final_state)
metrics = calculate_metrics(final_state)

print("\n==== METRICS ====")
for k, v in metrics.items():
    print(f"{k}: {v}")
    
print("\nDecision memo saved at:", file_path)