"""
Utility tools for executing Python code, managing packages, and performing system operations.
"""
from datetime import datetime
import os
import subprocess
import sys
from typing import Annotated, Optional

# Third-party imports
import matplotlib.pyplot as plt
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import ShellTool
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

# Local imports
from src.config import TAVILY_API_KEY

# Constants
SANDBOX_DIR = "sandbox"
CHARTS_DIR = os.path.join(SANDBOX_DIR, "charts")

# Initialize directories
os.makedirs(CHARTS_DIR, exist_ok=True)

# Initialize tools
tavily_tool = TavilySearchResults(max_results=5, tavily_api_key=TAVILY_API_KEY)
repl = PythonREPL()
bash_tool = ShellTool(
    description="Execute bash commands for system operations and file management. "
                "Use for reading files, checking system status, etc.",
)

def save_matplotlib_chart() -> Optional[str]:
    """Save matplotlib chart if one exists and return the filepath."""
    if not plt.get_fignums():
        return None
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chart_{timestamp}.png"
    filepath = os.path.join(CHARTS_DIR, filename)
    
    plt.savefig(filepath, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    
    return filepath

@tool
def python_repl(
    code: Annotated[str, "The Python code to execute in the REPL environment"]
) -> str:
    """
    Execute Python code in a REPL environment.
    
    Args:
        code: The Python code to execute
        
    Returns:
        str: Execution result or error message
        
    Note:
        For output, use print(...). Any generated charts will be automatically 
        saved to the sandbox/charts directory.
    """
    try:
        result = repl.run(code)
        
        # Handle chart saving if present
        chart_path = save_matplotlib_chart()
        
        output = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
        if chart_path:
            output = f"Successfully executed code and saved chart to {chart_path}\n" + output
            
        return output
    
    except Exception as e:
        return f"Failed to execute. Error: {repr(e)}"

@tool
def pip_install(
    package: Annotated[str, "The Python package name to install"]
) -> str:
    """
    Install Python packages using pip.
    
    Args:
        package: Name of the package to install (can include version specification)
        
    Returns:
        str: Success or error message
    """
    try:
        # Check if package is already installed
        package_name = package.split('==')[0]
        try:
            __import__(package_name)
            return f"Package {package} is already installed"
        except ImportError:
            pass

        # Install package
        process = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package, '--quiet'],
            capture_output=True,
            text=True
        )
        
        if process.returncode == 0:
            return f"Successfully installed {package}"
        return f"Failed to install {package}. Error: {process.stderr}"
        
    except Exception as e:
        return f"Installation failed with error: {str(e)}"