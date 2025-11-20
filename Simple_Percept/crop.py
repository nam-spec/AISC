class CropAgent:
    def __init__(self):
        pass

    def perceive(self, soil, rainfall, season):
        return {"soil": soil, "rainfall": rainfall, "season": season}

    def decide(self, percept):
        soil = percept["soil"]
        rain = percept["rainfall"]
        season = percept["season"]

        # RULE-SET
        if soil == "clay" and rain == "high":
            return "Rice"

        if soil == "sandy" and rain == "low":
            return "Millet"

        if soil == "loam" and rain == "medium":
            return "Wheat"

        if season == "summer":
            return "Cotton"

        if season == "winter":
            return "Mustard"

        if season == "monsoon":
            return "Rice"

        return "No suitable crop found"

    def act(self, recommendation):
        print("Recommended Crop:", recommendation)


# Simulation
agent = CropAgent()

soil = input("Enter soil type: ")
rain = input("Enter rainfall level: ")
season = input("Enter season: ")

percept = agent.perceive(soil, rain, season)

crop = agent.decide(percept)
agent.act(crop)
