import numpy as np

class MamdaniFIS:
    def __init__(self):
        self.rules = []

    # Add fuzzy rule: each rule is a tuple (antecedents, consequent)
    def add_rule(self, antecedents, consequent):
        self.rules.append((antecedents, consequent))

    # Membership function example: triangular
    def triangular_mf(self, x, a, b, c):
        return max(min((x - a)/(b - a), (c - x)/(c - b)), 0)

    # Evaluate rules for given inputs
    def evaluate(self, inputs):
        output_mfs = []
        for antecedents, consequent in self.rules:
            # Compute rule strength using min for AND
            strength = min([mf(inputs[var]) for var, mf in antecedents.items()])
            output_mfs.append((strength, consequent))
        return output_mfs

    # Aggregate outputs and defuzzify (centroid)
    def defuzzify(self, output_mfs, universe):
        aggregated = np.zeros_like(universe)
        for strength, mf_func in output_mfs:
            mf_values = np.array([min(strength, mf_func(x)) for x in universe])
            aggregated = np.maximum(aggregated, mf_values)
        # Centroid method
        if np.sum(aggregated) == 0:
            return 0
        return np.sum(aggregated * universe) / np.sum(aggregated)


# ---------------- Example usage (general) ----------------
# Define input membership functions
temp_mf = {
    "cold": lambda x: max(min((25-x)/(25-15), 1),0),
    "warm": lambda x: max(min((x-20)/(30-20), (40-x)/(40-30)),0),
    "hot":  lambda x: max(min((x-35)/(45-35),1),0)
}

humidity_mf = {
    "low": lambda x: max(min((50-x)/(50-30),1),0),
    "high": lambda x: max(min((x-40)/(60-40),1),0)
}

fan_speed_mf = {
    "slow": lambda x: max(min((30-x)/(30-10),1),0),
    "medium": lambda x: max(min((50-x)/(50-30),1),0),
    "fast": lambda x: max(min((70-x)/(70-50),1),0)
}

# Universe of discourse for output
fan_universe = np.linspace(0, 70, 100)

# Create Mamdani system
fis = MamdaniFIS()

# Add general rules (antecedent: input MFs, consequent: output MF)
fis.add_rule(
    antecedents={"temp": temp_mf["hot"], "humidity": humidity_mf["high"]},
    consequent=fan_speed_mf["fast"]
)
fis.add_rule(
    antecedents={"temp": temp_mf["cold"]},
    consequent=fan_speed_mf["slow"]
)

# Evaluate rules for crisp inputs
inputs = {"temp": 40, "humidity": 50}
output_mfs = fis.evaluate(inputs)

# Defuzzify to get crisp output
fan_speed = fis.defuzzify(output_mfs, fan_universe)
print("Crisp Fan Speed:", fan_speed)
