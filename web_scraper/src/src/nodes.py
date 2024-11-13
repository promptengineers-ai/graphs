from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

def scraper_node(state):
    """Mock scraper that pretends to fetch content from a URL"""
    url = state.get("url", "")
    
    # Mock response with detailed logging
    content = f"Mocked content scraped from {url}"
    return {
        "messages": [
            SystemMessage(content=f"Scraper Tool Logs: Starting scrape of {url}"),
            AIMessage(content=f"Successfully scraped content from {url}", name="Scraper"),
        ],
        "sender": "scraper",
        "documents": [content],
        "url": url
    }

def indexer_node(state):
    """Mock indexer that pretends to create vector embeddings"""
    docs = state.get("documents", [])
    
    # Mock indexing with detailed logging
    return {
        "messages": [
            SystemMessage(content=f"Indexer Tool Logs: Processing {len(docs)} documents"),
            AIMessage(content=f"Successfully created vector embeddings for {len(docs)} documents", name="Indexer"),
        ],
        "sender": "indexer",
        "documents": docs
    }

def searcher_node(state):
    """Mock searcher that pretends to search the vector store"""
    query = state.get("query", "")
    
    # Mock search with detailed logging
    results = [f"Mock result for query: {query}"]
    return {
        "messages": [
            SystemMessage(content=f"Search Tool Logs: Executing search for query: {query}"),
            AIMessage(content=f"Found {len(results)} relevant results:\n{results[0]}", name="Searcher"),
        ],
        "sender": "searcher",
        "results": results
    }

def supervisor_node(state):
    """Supervisor that coordinates the workflow"""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    
    if not last_message or isinstance(last_message, HumanMessage):
        # Initial state - start with scraping
        return {
            "messages": [
                SystemMessage(content="Supervisor analyzing request..."),
                AIMessage(content="I'll help coordinate the scraping and search process. Starting with web scraping.", name="Supervisor"),
            ],
            "sender": "supervisor",
            "url": "https://example.com"
        }
    
    if state.get("sender") == "scraper":
        return {
            "messages": [
                SystemMessage(content="Supervisor reviewing scrape results..."),
                AIMessage(content="Scraping complete. Now I'll initiate the indexing process to create vector embeddings.", name="Supervisor"),
            ],
            "sender": "supervisor"
        }
    
    if state.get("sender") == "indexer":
        return {
            "messages": [
                SystemMessage(content="Supervisor preparing search phase..."),
                AIMessage(content="Vector index created. Ready to perform semantic search.", name="Supervisor"),
            ],
            "sender": "supervisor",
            "query": "mock search query"
        }
    
    if state.get("sender") == "searcher":
        return {
            "messages": [
                SystemMessage(content="Supervisor finalizing process..."),
                AIMessage(content="FINAL ANSWER: Search process complete. I've gathered all relevant results.", name="Supervisor"),
            ],
            "sender": "supervisor"
        }

def router(state):
    """Routes the workflow based on supervisor's decision"""
    messages = state.get("messages", [])
    last_message = messages[-1]
    
    if "FINAL ANSWER" in last_message.content:
        return END
        
    if state.get("sender") == "supervisor":
        if "Starting with web scraping" in last_message.content:
            return "scrape"
        elif "initiate the indexing process" in last_message.content:
            return "index"
        elif "Ready to perform semantic search" in last_message.content:
            return "search"
    
    return "supervisor" 