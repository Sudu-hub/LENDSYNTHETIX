# src/core/workflow.py

from langgraph.graph import StateGraph, END
from src.core.state import WarRoomState
from src.agents.risk_agent import RiskAgent
from src.agents.sales_agent import SalesAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.moderator_agent import ModeratorAgent


# Instantiate agents
risk_agent = RiskAgent()
sales_agent = SalesAgent()
compliance_agent = ComplianceAgent()
moderator_agent = ModeratorAgent()


# ---------------------------
# Node functions
# ---------------------------

def risk_node(state: WarRoomState):
    print("Risk:")
    return risk_agent.evaluate(state)


def sales_node(state: WarRoomState):
    print("Sales:")
    return sales_agent.evaluate(state)


def compliance_node(state: WarRoomState):
    print("Compliance:")
    return compliance_agent.evaluate(state)


def moderator_node(state: WarRoomState):
    print("Moderator:")
    return moderator_agent.decide(state)


# ---------------------------
# Debate Router (PURE FUNCTION)
# ---------------------------

def debate_router(state: WarRoomState):

    # Stop loop if max rounds reached
    if state["debate_round"] >= state["max_rounds"]:
        return "compliance"

    # Continue debate only if risky AND strong growth
    if (
        state["risk_score"] is not None
        and state["risk_score"] < 70
        and state["loan_data"].revenue_growth > 0.25
    ):
        return "risk"

    # Otherwise move forward
    return "compliance"


# ---------------------------
# Build Graph
# ---------------------------

def build_graph():

    builder = StateGraph(WarRoomState)

    builder.add_node("risk", risk_node)
    builder.add_node("sales", sales_node)
    builder.add_node("compliance", compliance_node)
    builder.add_node("moderator", moderator_node)

    builder.set_entry_point("risk")

    # risk → sales
    builder.add_edge("risk", "sales")

    # sales → (debate loop OR compliance)
    builder.add_conditional_edges(
        "sales",
        debate_router,
        {
            "risk": "risk",
            "compliance": "compliance",
        },
    )

    # compliance → moderator
    builder.add_edge("compliance", "moderator")

    # moderator → END
    builder.add_edge("moderator", END)

    return builder.compile()