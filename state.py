from typing import TypedDict, List, Annotated
import operator
from pydantic import BaseModel, Field

class CodeSolution(BaseModel):
    """Structured output for the LLM's 'Golden Answer'"""
    explanation: str = Field(description="Step-by-step logic and reasoning")
    python_code: str = Field(description="The executable Python code block")
    complexity: str = Field(description="Time and Space complexity (Big O)")

class AgentState(TypedDict):
    """Main state managed by LangGraph"""
    task: str
    code_solution: CodeSolution
    error: str
    iterations: int
    history: Annotated[List[str], operator.add]