from openai import OpenAI
from config import OPENAI_API_KEY

# Setup OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)
# Connect to GPT Assistant
assistant = client.beta.assistants.retrieve("asst_dG9wU3z6RKNYWLvk2pTvalBr")
# Create an OpenAI Assistant Thread
global thread
thread = client.beta.threads.create()