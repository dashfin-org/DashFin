from composio import Composio
from openai   import OpenAI
from dotenv   import load_dotenv
import os, json

load_dotenv()  # Picks up .env if present
openai   = OpenAI()
composio = Composio()

user_id = "dashfin-admin@example.com"  # Any stable string for your user/org

# Get the GitHub toolkit’s functions
tools = composio.tools.get(user_id=user_id, toolkits=["GITHUB"])
print("[*] Tools schema:\n", json.dumps(tools, indent=2))

def invoke_llm(task="Create a branch 'ai/hello-file', add hello.txt and open a PR"):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": task}],
        tools=tools,
    )
    result = composio.provider.handle_tool_calls(user_id=user_id, response=completion)
    print("[*] LLM response:", completion)
    print("[*] Tool call result:", result)

if __name__ == "__main__":
    invoke_llm()
