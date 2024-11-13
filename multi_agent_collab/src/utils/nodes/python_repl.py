import functools

from src.agent import create_agent
from src.utils.tools import python_repl
from src.utils.nodes.common import agent_node, llm

# Rename chart_generator to python_repl_chain
python_repl_agent = create_agent(
    llm,
    [python_repl],
    system_message="""You are a Python REPL specialist. When executing code:
    1. Always save outputs to the sandbox/ directory (this is handled automatically)
    2. Never use plt.show() - outputs are automatically saved
    3. Focus on creating clear, well-formatted output
    4. Include appropriate labels and documentation
    5. After execution, report the filepath where any outputs were saved
    """,
)
python_repl_node = functools.partial(agent_node, agent=python_repl_agent, name="python_repl_chain")