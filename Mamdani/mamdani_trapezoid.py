import numpy as np

class MamdaniFIS:
    def __init__(self):
        self.rules = []

    def add_rule(self, antecedents, consequent):
        self.rules.append((antecedents, consequent))

    def triangular_mf(self, x, a, b, c):
        return max(min((x - a)/(b - a), (c - x)/(c - b)), 0)

    def trapezoidal_mf(self, x, a, b, c, d):
        if x <= a or x >= d:
            return 0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return 1
        elif c < x < d:
            return (d - x) / (d - c)

    def evaluate(self, inputs):
        output_mfs = []
        for antecedents, consequent in self.rules:
            # Compute rule strength (min for AND)
            strength = min([mf(inputs[var]) for var, mf in antecedents.items()])
            output_mfs.append((strength, consequent))
        return output_mfs

    def defuzzify(self, output_mfs, universe):
        aggregated = np.zeros_like(universe)
        for strength, mf_func in output_mfs:
            mf_values = np.array([min(strength, mf_func(x)) for x in universe])
            aggregated = np.maximum(aggregated, mf_values)
        if np.sum(aggregated) == 0:
            return 0
        return np.sum(aggregated * universe) / np.sum(aggregated)

# --------- Example Usage ---------
# Trapezoidal input MF
temp_mf = {
    "cold": lambda x: MamdaniFIS().trapezoidal_mf(x, 0, 0, 15, 20),
    "warm": lambda x: MamdaniFIS().trapezoidal_mf(x, 15, 20, 25, 30),
    "hot":  lambda x: MamdaniFIS().trapezoidal_mf(x, 25, 30, 40, 40)
}

fan_speed_mf = {
    "slow": lambda x: MamdaniFIS().triangular_mf(x, 0, 10, 30),
    "medium": lambda x: MamdaniFIS().triangular_mf(x, 20, 35, 50),
    "fast": lambda x: MamdaniFIS().triangular_mf(x, 40, 55, 70)
}

fan_universe = np.linspace(0, 70, 100)

fis = MamdaniFIS()
fis.add_rule(
    antecedents={"temp": temp_mf["hot"]},
    consequent=fan_speed_mf["fast"]
)
fis.add_rule(
    antecedents={"temp": temp_mf["cold"]},
    consequent=fan_speed_mf["slow"]
)

inputs = {"temp": 28}
output_mfs = fis.evaluate(inputs)
fan_speed = fis.defuzzify(output_mfs, fan_universe)
print("Crisp Fan Speed:", fan_speed)
