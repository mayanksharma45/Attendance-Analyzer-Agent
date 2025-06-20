from langgraph.graph import StateGraph
from langgraph.prebuilt import MessagesState

# Placeholder for Groq or any LLM completion
def fake_groq_response(attendance_data):
    present = sum(1 for a in attendance_data if a["Status"] == "Present")
    late = sum(1 for a in attendance_data if a["Status"] == "Late")
    absent = sum(1 for a in attendance_data if a["Status"] == "Absent")
    
    return f"Today, {present} students were present, {late} were late, and {absent} were absent."

# LangGraph-compatible node function
def summarize_attendance(state: dict) -> dict:
    messages = state.get("messages", [])
    
    # Extract last message that contains attendance list
    if messages and "content" in messages[-1]:
        attendance_data = messages[-1]["content"]
        response = fake_groq_response(attendance_data)
        
        messages.append({"role": "assistant", "content": response})
    else:
        messages.append({"role": "assistant", "content": "No attendance data provided."})
    
    return {"messages": messages}

# Build LangGraph agent
def build_agent():
    builder = StateGraph(MessagesState)
    builder.add_node("summarizer", summarize_attendance)
    builder.set_entry_point("summarizer")
    return builder.compile()
