class ClassroomAgent:

    def __init__(self):
        self.lights = "OFF"
        self.fans = "OFF"

    def perceive(self, occupancy, light_level, temp):
        return {
            "occupancy": occupancy,
            "light": light_level,
            "temp": temp
        }

    def decide(self, percept):
        occupancy = percept["occupancy"]
        light_level = percept["light"]
        temp = percept["temp"]

        # Rule 1: If no one is in the classroom
        if occupancy == 0:
            self.lights = "OFF"
            self.fans = "OFF"
            return "Classroom empty → Turning OFF all appliances."

        # Rule 2: People present but sunlight is low
        if occupancy > 0 and light_level < 40:
            self.lights = "ON"
        else:
            self.lights = "OFF"

        # Rule 3: Temperature check
        if temp > 28:
            self.fans = "ON"
        else:
            self.fans = "OFF"

        return f"Lights: {self.lights}, Fans: {self.fans}"

    def act(self, action_msg):
        print("Agent:", action_msg)


# ---------------- Simulation ----------------
agent = ClassroomAgent()

percept = agent.perceive(occupancy=20, light_level=30, temp=32)
action = agent.decide(percept)
agent.act(action)
