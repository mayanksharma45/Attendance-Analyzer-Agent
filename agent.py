from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import Tool
from utils.llms import LLMModel1
from toolkit.tools import parse_transcript_tool_func, update_sheet_tool_func
from prompt_library.prompt import SYSTEM_PROMPT


class AttendanceAnalyzerAgent:
    def __init__(self):
        llm_model = LLMModel1()
        self.llm = llm_model.get_model1()
        self.system_prompt = SYSTEM_PROMPT

        self.tools = [
            Tool.from_function(
                func=parse_transcript_tool_func,
                name="TranscriptParserTool",
                description="Parse a transcript text string and return JSON records of attendance."
            ),
            Tool.from_function(
                func=update_sheet_tool_func,
                name="SheetUpdaterTool",
                description="Save JSON attendance data into an Excel sheet."
            )
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def _reasoning_node(self, state: MessagesState) -> dict:
        full_prompt = [self.system_prompt] + state["messages"]
        response = self.llm_with_tools.invoke(full_prompt)

        if isinstance(response, str):
            response = AIMessage(content=response)

        return {"messages": state["messages"] + [response]}

    @staticmethod
    def should_continue(state: MessagesState) -> str:
        print("Evaluating stop condition. Messages so far:")
        for msg in reversed(state["messages"]):
            print(f"{msg.type}: {msg.content}")
            if hasattr(msg, "content") and isinstance(msg.content, str):
                content = msg.content.lower()
                if "sheet updated" in content or "✅" in content:
                    print("✅ Ending condition met.")
                    return END
        print("🔁 Continuing...")
        return "tools"

    def build(self):
        builder = StateGraph(MessagesState)

        builder.add_node("agent", self._reasoning_node)
        builder.add_node("tools", ToolNode(self.tools))

        builder.set_entry_point("agent")
        builder.add_conditional_edges("agent", self.should_continue)
        builder.add_edge("tools", "agent")

        return builder.compile()

