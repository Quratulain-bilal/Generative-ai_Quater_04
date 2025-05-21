from dataclasses import dataclass

@dataclass
class Agent:
    instructions: str

    def __call__(self, message: str) -> str:
        return f"[{self.instructions}] ➤ {message}"

# Example usage
travel_bot = Agent("You are a helpful travel planner. Be polite and brief.")
print(travel_bot("Plan my trip to Tokyo."))
