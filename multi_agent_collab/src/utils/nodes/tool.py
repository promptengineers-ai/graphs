from langgraph.prebuilt import ToolNode
from src.utils.tools import tavily_tool, python_repl, pip_install, bash_tool

tools = [tavily_tool, python_repl, pip_install, bash_tool]
tool_node = ToolNode(tools)