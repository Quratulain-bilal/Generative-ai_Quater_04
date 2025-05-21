from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    role: str

# Instance banate waqt constructor ki zarurat nahi
bot = Agent(name="WeatherBot", role="Weather Info Provider")

print(bot)
