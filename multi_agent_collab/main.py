from src.graph import compile
from langchain_core.messages import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod



TASK = ("""Use the python_repl_chain to...
1. Fetch last month of close prices for Solana.
2. Save the chart to the sandbox/charts directory.
3. Report the filepath of the saved chart.

Use the bash_chain to...
1. Get the current date and time.""")


graph = compile()
events = graph.stream(
    {"messages": [HumanMessage(content=TASK)]},
    # Maximum number of steps to take in the graph
    {"recursion_limit": 30},
)

# Display the graph and wait for user input before continuing
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = f"./sandbox/graphs/{timestamp}_graph.png"
try:
    graph_image_path = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
        output_file_path=output_file_path
    )
    print(f"Graph image saved to: {output_file_path}")
except ImportError:
    ascii_graph = graph.get_graph().draw_ascii()
    with open(f"./sandbox/graphs/{timestamp}_graph.txt", "w") as f:
        f.write(ascii_graph)
    print(f"Graph ASCII art saved to: ./sandbox/graphs/{timestamp}_graph.txt")

for step, event in enumerate(events, 1):
    print(f"\n--- Step {step} ---")
    
    # Print the event key and its contents
    for key, value in event.items():
        print(f"\nNode: {key}")
        if 'messages' in value:
            for msg in value['messages']:
                role = msg.__class__.__name__.replace('Message', '')
                content = msg.content
                print(f"Role: {role}")
                print(f"Content:\n{content}")
        else:
            print("No messages in this component")
    
    print("\n" + "=" * 50)