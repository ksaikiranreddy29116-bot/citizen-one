from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.agents.welfare_agents import run_recommendation_agent, run_reminder_agent

class CitizenOneState(TypedDict):
    user_profile: dict
    recommendations: dict
    notifications: list

def recommendation_node(state: CitizenOneState):
    recs = run_recommendation_agent(state["user_profile"])
    return {"recommendations": recs}

def reminder_node(state: CitizenOneState):
    notifs = run_reminder_agent(state["user_profile"])
    return {"notifications": notifs}

# Build LangGraph Engine
workflow = StateGraph(CitizenOneState)
workflow.add_node("recommendation_engine", recommendation_node)
workflow.add_node("reminder_engine", reminder_node)

workflow.add_edge(START, "recommendation_engine")
workflow.add_edge("recommendation_engine", "reminder_engine")
workflow.add_edge("reminder_engine", END)

citizen_one_pipeline = workflow.compile()