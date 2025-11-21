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




// java
class TrafficSignalAgent {

    private String currentSignal;

    public TrafficSignalAgent() {
        currentSignal = "North";
    }

    // Perception values stored separately
    int northCars, southCars, eastCars, westCars;
    String emergency;

    // Perceive method
    public void perceive(int north, int south, int east, int west, String emergencySide) {
        northCars = north;
        southCars = south;
        eastCars = east;
        westCars = west;
        emergency = emergencySide;
    }

    // Decide which signal should be green
    public String decide() {

        // 1. Emergency condition overrides everything
        if (emergency.equalsIgnoreCase("north")) return "North";
        if (emergency.equalsIgnoreCase("south")) return "South";
        if (emergency.equalsIgnoreCase("east"))  return "East";
        if (emergency.equalsIgnoreCase("west"))  return "West";

        // 2. Find direction with maximum vehicles
        int maxCars = northCars;
        String maxSide = "North";

        if (southCars > maxCars) {
            maxCars = southCars;
            maxSide = "South";
        }
        if (eastCars > maxCars) {
            maxCars = eastCars;
            maxSide = "East";
        }
        if (westCars > maxCars) {
            maxCars = westCars;
            maxSide = "West";
        }

        // 3. If traffic is heavy (>5 cars), extend green for that direction
        if (maxCars > 5) {
            return maxSide;
        } else {
            // Otherwise go to next direction in cycle
            return nextSignal();
        }
    }

    // Cyclic order: North -> East -> South -> West -> North ...
    public String nextSignal() {
        String[] order = {"North", "East", "South", "West"};

        int index = 0;
        for (int i = 0; i < order.length; i++) {
            if (order[i].equalsIgnoreCase(currentSignal)) {
                index = i;
                break;
            }
        }

        return order[(index + 1) % 4];
    }

    // Perform the action
    public void act(String action) {
        System.out.println("Green signal → " + action);
        currentSignal = action;
    }

    // MAIN simulation
    public static void main(String[] args) {

        TrafficSignalAgent agent = new TrafficSignalAgent();

        agent.perceive(
                3,   // north cars
                10,  // south cars
                2,   // east cars
                1,   // west cars
                "none" // emergency
        );

        String action = agent.decide();
        agent.act(action);
    }
}
//
