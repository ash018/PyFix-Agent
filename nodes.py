import sys
import io
from langchain_openai import ChatOpenAI
from state import AgentState, CodeSolution

llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def generate_node(state: AgentState):
    """Generates or repairs code based on current state and errors."""
    prompt = f"Task: {state['task']}\n"
    if state['error'] != "none":
        prompt += f"Previous Error: {state['error']}\nFix the code below."
    
    # Use structured output for 'Golden Standard' responses
    structured_llm = llm.with_structured_output(CodeSolution)
    response = structured_llm.invoke(prompt)
    
    return {"code_solution": response, "iterations": state['iterations'] + 1}

def execute_node(state: AgentState):
    """Safely executes the code and captures tracebacks."""
    code = state['code_solution'].python_code
    output_capture = io.StringIO()
    sys.stdout = output_capture
    
    try:
        # Standard Python exec() within a controlled scope
        exec(code, {"__builtins__": __builtins__}, {})
        sys.stdout = sys.__stdout__
        return {"error": "none"}
    except Exception as e:
        sys.stdout = sys.__stdout__
        return {"error": str(e)}