
import os
from dotenv import load_dotenv
from rich import print as rprint

# OpenAI SDK or compatible wrapper
from agents import (
    function_tool,Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel,handoffs
)

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# Setup external client
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the model
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

# ----------- TOOLS -----------
@function_tool
def get_current_location() -> str:
    """Returns the user's current location (mock)."""
    return "Lahore, Pakistan"

@function_tool
def get_breaking_news() -> str:
    """Returns mock breaking news."""
    return "Breaking News: Heavy rains expected in Lahore today."



PlantAgent = Agent(
    name="PlantAgent",
    instructions="""
You are a Plant Expert. You only talk about plants, such as watering, sunlight, growth tips, and how to take care of different plant species.
""",
)


MainAgent = Agent(
    name="MainAgent",
    instructions="""
You are a helpful assistant. You respond using tools when needed or hand off the task to the PlantAgent 
if the question is about plants or gardening.
""",
    tools=[get_current_location, get_breaking_news],
    handoffs=[PlantAgent],
    model=model
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

runner = Runner()  

Result = runner.run_sync(
    MainAgent,
    """
    1. What is my current location?,
    2. Any breaking news?,
    3. What is photosynthesis?
    """,
    run_config=config
)

print(Result.final_output)
