import os
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from sample_agent.agent import graph # the coagents-starter path, replace this if its different

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="sample_agent", # the name of your agent defined in langgraph.json
            description="Describe your agent here, will be used for multi-agent orchestration",
            graph=graph, # the graph object from your langgraph import
        )
    ],
)

# Use CopilotKit's FastAPI integration to add a new endpoint for your LangGraph agents
add_fastapi_endpoint(app, sdk, "/copilotkit", use_thread_pool=False)

# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "sample_agent.demo:app", # the path to your FastAPI file, replace this if its different
        host="0.0.0.0",
        port=port,
        reload=True,
    )

if __name__ == "__main__":
    main()