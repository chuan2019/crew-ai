# Corrected example for CrewAI with Ollama
from crewai import Agent, LLM
from crewai.tools import BaseTool

# -------------------------
# 1. Configure your local Ollama LLM
# -------------------------
ollama_llm = LLM(
    model="ollama/mistral:latest",      # CrewAI provider format
    base_url="http://localhost:11434",  # Ollama local API
    temperature=0.7,
)

# -------------------------
# 2. Define a tool by subclassing BaseTool
# -------------------------
class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Evaluates simple arithmetic expressions"

    def _run(self, query: str) -> str:
        try:
            return str(eval(query))
        except Exception as e:
            return f"Error: {e}"

calculator = CalculatorTool()

# -------------------------
# 3. Create an agent
# -------------------------
agent = Agent(
    role="Local Ollama Assistant",
    goal="Answer user questions accurately and use tools for arithmetic when needed.",
    backstory="You are a practical AI assistant running locally with access to a calculator tool.",
    llm=ollama_llm,
    tools=[calculator],
    max_iter=3
)

# -------------------------
# 4. Interact with the agent
# -------------------------
user_prompt = "What is 12 * 15? And tell me a fun fact about space."

response = agent.kickoff(user_prompt)

print("Agent Response:\n", getattr(response, "raw", response))