from functools import partial

from src.agent import create_agent
from src.utils.nodes.common import agent_node, llm
from src.utils.tools import pip_install, bash_tool

# Update the bash chain (formerly package installer)
bash_prompt = """You are a system operations specialist with access to bash commands.

Your primary responsibilities:
1. Execute bash commands to:
   - Perform system operations
   - Manage files and directories
   - Check system status

When executing commands:
- Use bash_tool for all operations
- Always verify command execution success
- Report any errors or issues clearly"""

bash_agent = create_agent(
    llm,
    [pip_install, bash_tool],
    system_message=bash_prompt
)

bash_node = partial(
    agent_node,
    agent=bash_agent,
    name="bash_chain"
)