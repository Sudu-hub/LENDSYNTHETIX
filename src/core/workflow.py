# src/core/workflow.py

from langgraph.graph import StateGraph, END
from langsmith import traceable

from src.core.state import WarRoomState
from src.rag.pdf_loader import extract_loan_data_from_pdf

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
# Document Processing Node
# ---------------------------

@traceable(name="document_processing")
def document_node(state: WarRoomState):

    print("📄 Reading loan PDF")

    pdf_path = state["pdf_path"]

    loan_data = extract_loan_data_from_pdf(pdf_path)

    state["loan_data"] = loan_data

    return state


# ---------------------------
# Agent Nodes
# ---------------------------

@traceable(name="risk_node")
def risk_node(state: WarRoomState):

    print("⚠ Risk Agent Running")

    state["turn_count"] += 1
    state["debate_round"] += 1

    return risk_agent.evaluate(state)


@traceable(name="sales_node")
def sales_node(state: WarRoomState):

    print("📈 Sales Agent Running")

    state["turn_count"] += 1

    return sales_agent.evaluate(state)


@traceable(name="compliance_node")
def compliance_node(state: WarRoomState):

    print("🛡 Compliance Agent Running")

    state["turn_count"] += 1

    return compliance_agent.evaluate(state)


@traceable(name="moderator_node")
def moderator_node(state: WarRoomState):

    print("🎯 Moderator Finalizing Decision")

    state["turn_count"] += 1

    return moderator_agent.decide(state)


# ---------------------------
# Debate Router
# ---------------------------

def debate_router(state: WarRoomState):

    risk_score = state.get("risk_score")
    growth = state["loan_data"].revenue_growth

    rounds = state.get("debate_round", 0)
    max_rounds = state.get("max_rounds", 2)

    if rounds >= max_rounds:
        return "compliance"

    if risk_score and risk_score < 70 and growth > 0.25:
        return "risk"

    return "compliance"


# ---------------------------
# Build Graph
# ---------------------------

def build_graph(checkpointer=None):

    builder = StateGraph(WarRoomState)

    builder.add_node("document_processing", document_node)
    builder.add_node("risk", risk_node)
    builder.add_node("sales", sales_node)
    builder.add_node("compliance", compliance_node)
    builder.add_node("moderator", moderator_node)

    builder.set_entry_point("document_processing")

    builder.add_edge("document_processing", "risk")
    builder.add_edge("risk", "sales")

    builder.add_conditional_edges(
        "sales",
        debate_router,
        {
            "risk": "risk",
            "compliance": "compliance"
        },
    )

    builder.add_edge("compliance", "moderator")
    builder.add_edge("moderator", END)

    graph = builder.compile(checkpointer=checkpointer)

    return graph