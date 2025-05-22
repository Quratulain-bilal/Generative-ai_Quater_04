from typing import TypeVar, Generic

TContext = TypeVar('TContext')

class Agent(Generic[TContext]):
    def __init__(self, context: TContext):
        self.context = context

# String context
agent1 = Agent[str]("Yeh ek string context hai")

# Dict context
agent2 = Agent[dict]({"city": "Karachi", "temp": 32})
