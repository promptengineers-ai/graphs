from src.graph import compile
from langchain_core.messages import HumanMessage
from utils.visualize import visualize_graph

def main():
    # Compile the graph
    graph = compile()
    
    # Visualize the graph structure
    visualize_graph(graph)
    
    # Run the graph
    events = graph.stream(
        {
            "messages": [
                HumanMessage(content="Please scrape https://example.com and find relevant information about AI")
            ]
        },
        {"recursion_limit": 10}
    )
    
    # Print events in a chat-like format
    for step, event in enumerate(events, 1):
        for key, value in event.items():
            if 'messages' in value:
                for msg in value['messages']:
                    # Get the role and name
                    role = msg.__class__.__name__.replace('Message', '')
                    name = getattr(msg, 'name', role)
                    
                    # Format based on message type
                    if role == 'System':
                        print(f"\n🔧 {msg.content}")
                    elif role == 'AI':
                        print(f"\n🤖 {name}: {msg.content}")
                    elif role == 'Human':
                        print(f"\n👤 User: {msg.content}")
                    
                    print("─" * 80)

if __name__ == "__main__":
    main() 