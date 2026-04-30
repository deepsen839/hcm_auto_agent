# app/agent.py

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from app.tools import (
    log_interaction_tool,
    compliance_validation_tool,
    followup_scheduler_tool,
    hcp_recommendation_tool,
    final_finaloutput_tool
)
# =========================
# STATE
# =========================

class AgentState(TypedDict):

    user_input: str

    interaction_data: dict

    compliance_result: dict

    recommendations: list

    followup_tasks: list

    final_output: dict
    current_datetime: str | None = None


# =========================
# TOOL NODES
# =========================

def log_interaction_node(state: AgentState):

    existing_data = state.get(
        "interaction_data",
        {}
    )

    result = log_interaction_tool(

    state["user_input"],

    existing_data,

    state.get(
        "current_datetime"
    )

)

    return {
        "interaction_data": result
    }


def compliance_node(state: AgentState):

    result = compliance_validation_tool(
        state["interaction_data"]
    )

    return {
        "compliance_result": result
    }


def recommendation_node(state: AgentState):

    result = hcp_recommendation_tool(
        state["interaction_data"]
    )

    return {
        "recommendations": result
    }


def followup_node(state: AgentState):

    result = followup_scheduler_tool(
        state["interaction_data"]
    )

    return {
        "followup_tasks": result
    }


def final_node(state: AgentState):

    return final_finaloutput_tool(state)
    


# =========================
# GRAPH
# =========================

workflow = StateGraph(AgentState)

workflow.add_node(
    "log_interaction",
    log_interaction_node
)

workflow.add_node(
    "compliance_check",
    compliance_node
)

workflow.add_node(
    "recommendations",
    recommendation_node
)

workflow.add_node(
    "followup_scheduler",
    followup_node
)

workflow.add_node(
    "finalize",
    final_node
)

# =========================
# FLOW
# =========================

workflow.set_entry_point("log_interaction")

workflow.add_edge(
    "log_interaction",
    "compliance_check"
)

workflow.add_edge(
    "compliance_check",
    "recommendations"
)

workflow.add_edge(
    "recommendations",
    "followup_scheduler"
)

workflow.add_edge(
    "followup_scheduler",
    "finalize"
)

workflow.add_edge(
    "finalize",
    END
)

# =========================
# COMPILE
# =========================

agent = workflow.compile()