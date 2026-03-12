from developer import DeveloperAgent

agent = DeveloperAgent()

# Try calling it
try:
    agent.generate_code("story", "design", "rfp", "proj123")
    print("Call succeeded → 4 arguments are accepted")
except TypeError as e:
    print("Error:", e)
    