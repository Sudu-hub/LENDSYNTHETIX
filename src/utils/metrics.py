def calculate_metrics(state):

    return {
        "consensus_speed_turns": state["turn_count"],
        "debate_rounds": state["debate_round"],
        "risk_score": state["risk_score"],
        "compliance_veto": state["veto"],
        "final_decision": state["final_decision"],
        "total_flags": len(state["flags"]),
    }