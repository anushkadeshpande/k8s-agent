import subprocess
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

def run_kubectl(command: str):
    """
    Runs a kubectl command safely.
    Example: get pods, scale deployment frontend --replicas=3
    """
    try:
        cmd = ["kubectl"] + command.split()
        output = subprocess.check_output(cmd, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output or str(e)

tools = [
    Tool(
        name="KubectlTool",
        func=run_kubectl,
        description="Run kubectl commands to interact with Kubernetes cluster. "
                    "Example: 'get pods', 'get services', 'scale deployment frontend --replicas=3'."
    )
]

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# Example interactions
# print(agent.run("List all pods in the default namespace"))
# print(agent.run("Scale the deployment called frontend to 3 replicas"))
# print(agent.run("Get logs of the pod named backend-abc123"))
