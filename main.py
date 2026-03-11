from src.core.workflow import build_graph
from src.core.state import WarRoomState
from src.utils.audit_export import export_memo_to_pdf
from src.utils.metrics import calculate_metrics


# ---------------------------
# Build LangGraph
# ---------------------------

graph = build_graph()


# ---------------------------
# Initial State
# ---------------------------

state: WarRoomState = {

    # Document Input
    "pdf_path": "data/loan_application.pdf",

    # Loan data (filled after PDF parsing)
    "loan_data": None,

    # Agent opinions
    "sales_opinion": None,
    "risk_opinion": None,
    "compliance_opinion": None,

    # Risk flags
    "flags": [],
    "veto": False,

    # Debate tracking
    "turn_count": 0,
    "debate_round": 0,
    "max_rounds": 2,
    "consensus_reached": False,

    # Risk evaluation
    "risk_score": None,

    # Final decision
    "final_decision": None,
    "decision_summary": None,
}


# ---------------------------
# Run Graph
# ---------------------------

final_state = graph.invoke(state)


# ---------------------------
# Optional: Streaming Output
# ---------------------------

print("\n--- Agent Debate ---\n")


# ---------------------------
# Export Decision Memo
# ---------------------------

file_path = export_memo_to_pdf(final_state)


# ---------------------------
# Calculate Metrics
# ---------------------------

metrics = calculate_metrics(final_state)

print("\n==== METRICS ====")

for k, v in metrics.items():
    print(f"{k}: {v}")


print("\nDecision memo saved at:", file_path)