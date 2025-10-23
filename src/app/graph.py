"""
A very simple LangGrange with one Node
- Node 'summarize_ticket' given a user message, interrupt it as a support ticket
and produce a short summary + suggest priority

Real example to learn from:
Input: "Our checkout throw 500 when applying a coupon SAVE10, Affects ~10% users."
Output: "Issue: 500 on coupon SAVE10 during checkout; Scope ~10%. Priority: High."
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from llm import call_gemini

def summarize_ticket(state: Dict[str, Any]) -> Dict[str, Any]:
    message = state["message"] # Input message from user
    prompt = f"""
    You are a helpful assistant that summarizes support tickets.
    Given the ticket text delimited by <tickt> tag, output:
    - one line summary (Issue _+ Context)
    - Suggested Priority (Low/Medium/High)
    <ticket>
    {message}
    Answer in two lines:
    Summary: ...
    Priority: ...
    """

    result = call_gemini(prompt) # This is still we need to build
    return {"result": result}


# Build the graph
def build_graph():
    g = StateGraph(dict)
    g.add_node("summarize_ticket", summarize_ticket)
    g.add_edge(START, "summarize_ticket")
    g.add_edge("summarize_ticket", END)
    return  g.compile()


# A single agent graph
_graph = build_graph()

def run_graph(message: str) -> str:
    graph_input = {"message": message}
    out = _graph.invoke(graph_input)
    return out["result"]


# while True:
#     user_input = input("Enter: ")
#     print(f"👮🏻‍♂️Human Message: {user_input}")
#     ai_response = run_graph(user_input)
#     print(f"🤖AI Message: {ai_response}")