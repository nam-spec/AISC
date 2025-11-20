class TrafficSignalAgent:
    def __init__(self):
        self.current_signal = "North"

    def perceive(self, north, south, east, west, emergency):
        return {
            "north": north,
            "south": south,
            "east": east,
            "west": west,
            "emergency": emergency
        }

    def decide(self, percept):
        roads = ["north", "south", "east", "west"]

        # Emergency rule: override everything
        if percept["emergency"] in roads:
            return percept["emergency"]

        # Choose direction with max vehicles
        max_side = max(roads, key=lambda r: percept[r])
        max_cars = percept[max_side]

        # Rule: above threshold → extend green
        if max_cars > 5:
            return max_side
        else:
            return self.next_signal()

    def next_signal(self):
        order = ["North", "East", "South", "West"]
        i = order.index(self.current_signal)
        return order[(i + 1) % 4]

    def act(self, action):
        print(f"Green signal → {action}")
        self.current_signal = action.capitalize()


# Simulation
agent = TrafficSignalAgent()

percept = agent.perceive(
    north=3, south=10, east=2, west=1,
    emergency="none"
)

action = agent.decide(percept)
agent.act(action)
