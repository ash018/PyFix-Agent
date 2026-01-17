from langgraph.graph import StateGraph, START, END
from nodes import generate_node, execute_node
from state import AgentState

def should_continue(state: AgentState):
    """Conditional router: checks if code works or max retries reached."""
    if state["error"] == "none" or state["iterations"] >= 3:
        return END
    return "generate"

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("generate", generate_node)
workflow.add_node("execute", execute_node)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "execute")
workflow.add_conditional_edges("execute", should_continue)

app = workflow.compile()