from julep import Client
import yaml
import time
import dotenv
import os

dotenv.load_dotenv()
JULEP_API_KEY = os.getenv("JULEP_API_KEY")

# Initialize the client
client = Client(api_key=JULEP_API_KEY)

# Create the agent
agent = client.agents.create(
  name="Julep Browser Use Agent"
#   description="A Julep agent that can use the computer tool to interact with the browser.",
)

# Load the task definition
with open('./research_agent.yaml', 'r') as file:
  task_definition = yaml.safe_load(file)

# Create the task
task = client.tasks.create(
  agent_id=agent.id,
  **task_definition
)

# Create the execution
execution = client.executions.create(
    task_id=task.id,
    input={
        "topic": "artificial intelligence in medical",
        "num_questions": 5
    }
)

# Wait for the execution to complete
while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
    print(result.status)
    time.sleep(1)

# Print the result
if result.status == "succeeded":
    print(result.output)
else:
    print(f"Error: {result.error}")
