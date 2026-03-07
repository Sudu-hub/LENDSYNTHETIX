# src/core/workflow.py

from langgraph.graph import StateGraph, END
from langsmith import traceable

from src.core.state import WarRoomState

from src.agents.risk_agent import RiskAgent
from src.agents.sales_agent import SalesAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.moderator_agent import ModeratorAgent


# ---------------------------
# Instantiate Agents
# ---------------------------

risk_agent = RiskAgent()
sales_agent = SalesAgent()
compliance_agent = ComplianceAgent()
moderator_agent = ModeratorAgent()


# ---------------------------
# Node Functions
# ---------------------------

@traceable(name="risk_node", metadata={"agent": "risk"})
def risk_node(state: WarRoomState):

    print("Risk Agent Running")

    state["turn_count"] += 1
    state["debate_round"] += 1

    return risk_agent.evaluate(state)


@traceable(name="sales_node", metadata={"agent": "sales"})
def sales_node(state: WarRoomState):

    print("Sales Agent Running")

    state["turn_count"] += 1

    return sales_agent.evaluate(state)


@traceable(name="compliance_node", metadata={"agent": "compliance"})
def compliance_node(state: WarRoomState):

    print("Compliance Agent Running")

    state["turn_count"] += 1

    return compliance_agent.evaluate(state)


@traceable(name="moderator_node", metadata={"agent": "moderator"})
def moderator_node(state: WarRoomState):

    print("Moderator Agent Running")

    state["turn_count"] += 1

    return moderator_agent.decide(state)


# ---------------------------
# Debate Router
# ---------------------------

@traceable(name="debate_router")
def debate_router(state: WarRoomState):

    risk_score = state.get("risk_score")
    growth = state["loan_data"].revenue_growth
    rounds = state.get("debate_round", 0)
    max_rounds = state.get("max_rounds", 2)

    # Stop debate if max rounds reached
    if rounds >= max_rounds:
        print("Max debate rounds reached → Compliance")
        return "compliance"

    # Continue debate if growth is strong but risk still unclear
    if risk_score is not None and risk_score < 70 and growth > 0.25:
        print("Debate continues → Back to Risk Agent")
        return "risk"

    print("Debate finished → Compliance Review")
    return "compliance"


# ---------------------------
# Build Graph
# ---------------------------

@traceable(name="build_warroom_graph")
def build_graph(checkpointer=None):

    builder = StateGraph(WarRoomState)

    # Nodes
    builder.add_node("risk", risk_node)
    builder.add_node("sales", sales_node)
    builder.add_node("compliance", compliance_node)
    builder.add_node("moderator", moderator_node)

    # Entry
    builder.set_entry_point("risk")

    # Debate Flow
    builder.add_edge("risk", "sales")

    builder.add_conditional_edges(
        "sales",
        debate_router,
        {
            "risk": "risk",
            "compliance": "compliance",
        },
    )

    builder.add_edge("compliance", "moderator")

    builder.add_edge("moderator", END)

    graph = builder.compile(checkpointer=checkpointer)

    return graph