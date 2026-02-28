from langgraph.graph import StateGraph, END
from src.core.state import WarRoomState
from src.agents.risk_agent import RiskAgent
from src.agents.sales_agent import SalesAgent
from src.agents.compliance_agent import ComplianceAgent
from src.agents.moderator_agent import ModeratorAgent


risk_agent = RiskAgent()
sales_agent = SalesAgent()
compliance_agent = ComplianceAgent()
moderator_agent = ModeratorAgent()


# Node functions
def risk_node(state: WarRoomState):
    return risk_agent.evaluate(state)


def sales_node(state: WarRoomState):
    return sales_agent.evaluate(state)


def compliance_node(state: WarRoomState):
    return compliance_agent.evaluate(state)


def moderator_node(state: WarRoomState):
    return moderator_agent.decide(state)


# Conditional routing after compliance
def compliance_router(state: WarRoomState):
    if state["veto"]:
        return "moderator"
    return "moderator"


def build_graph():
    builder = StateGraph(WarRoomState)

    builder.add_node("risk", risk_node)
    builder.add_node("sales", sales_node)
    builder.add_node("compliance", compliance_node)
    builder.add_node("moderator", moderator_node)

    builder.set_entry_point("risk")

    builder.add_edge("risk", "sales")
    builder.add_edge("sales", "compliance")

    builder.add_conditional_edges(
        "compliance",
        compliance_router,
        {
            "moderator": "moderator"
        },
    )

    builder.add_edge("moderator", END)

    return builder.compile()