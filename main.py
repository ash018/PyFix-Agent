import os
from dotenv import load_dotenv
from graph import app

# Load environment variables (API Keys)
load_dotenv()

def run_test_case(task_description: str):
    print("\n" + "="*50)
    print(f"STARTING TASK: {task_description[:60]}...")
    print("="*50)
    
    # Initialize the graph state
    initial_state = {
        "task": task_description,
        "code_solution": None,
        "error": "none",
        "iterations": 0,
        "history": []
    }
    
    
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"\n[Node: {key}]")
            if key == "generate":
                print(f"Refinement Iteration: {value['iterations']}")
                print(f"Plan: {value['code_solution'].explanation[:100]}...")
            elif key == "execute":
                status = "Success" if value['error'] == "none" else f"Error: {value['error']}"
                print(f"Execution Status: {status}")

    # Final result retrieval
    final_state = app.get_state({"configurable": {"thread_id": "1"}}).values # Simplification
    # Note: In production, you'd use a thread_id and checkpointer
    print("\n" + "="*50)
    print(" FINAL VERDICT: Task Completed Successfully.")

if __name__ == "__main__":
    # Test Case 1: Complex logic (Handling Nested JSON and Math)
    # This often causes "KeyError" or "TypeError" in first-shot LLM code.
    task_1 = """
    Write a function 'analyze_sales' that takes a nested JSON of sales data:
    {'2023': [{'month': 'Jan', 'amount': 100}, {'month': 'Feb', 'amount': '200'}]}
    The function must:
    1. Clean the 'amount' field (handle strings or ints).
    2. Calculate the average sales per month across all years provided.
    3. Return a dictionary with years as keys and their averages as values.
    """
    
    # Test Case 2: Algorithmic Edge Case (Sliding Window)
    task_2 = """
    Write a function 'longest_unique_substring' that returns the length of the longest 
    substring without repeating characters. 
    Include a test call for the string 'pwwkew' and print the result.
    """

    # Running the Agent
    run_test_case(task_1)
    run_test_case(task_2)