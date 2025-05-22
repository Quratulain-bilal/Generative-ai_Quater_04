# 👨‍💻 Agent class
class TravelAgent:
    system_prompt = "Main aik travel planner hoon."

    @classmethod
    def run(cls, user_prompt):
        return f"{cls.system_prompt} Aap ne pucha: '{user_prompt}'"

# 📞 User calling the agent directly without creating object
response = TravelAgent.run("Mujhe Turkey ka tour plan chahiye.")

print(response)
