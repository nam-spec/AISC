import numpy as np

# Membership functions
def triangular_mf(x, a, b, c):
    return max(min((x-a)/(b-a), (c-x)/(c-b)), 0) if a < b < c else 0

def trapezoidal_mf(x, a, b, c, d):
    return max(min((x-a)/(b-a), 1, (d-x)/(d-c)), 0) if a < b <= c < d else 0

# Example input & output variables with fuzzy sets and membership functions
input_vars = {
    'temperature': {
        'cold': lambda x: trapezoidal_mf(x, 0, 0, 10, 20),
        'warm': lambda x: triangular_mf(x, 15, 25, 35),
        'hot':  lambda x: trapezoidal_mf(x, 30, 40, 50, 50),
    }
}

output_vars = {
    'fan_speed': {
        'low':    lambda x: trapezoidal_mf(x, 0, 0, 0.2, 0.4),
        'medium': lambda x: triangular_mf(x, 0.3, 0.5, 0.7),
        'high':   lambda x: trapezoidal_mf(x, 0.6, 0.8, 1.0, 1.0),
    }
}

# Rule base matrix: rows input fuzzy sets, cols output fuzzy sets
input_terms = ['cold', 'warm', 'hot']
output_terms = ['low', 'medium', 'high']

# Example rule base (if temp is X then fan speed is Y)
rule_base = np.array([
    [1, 0, 0],  # cold -> low
    [0, 1, 0],  # warm -> medium
    [0, 0, 1],  # hot -> high
])

# Step 1: Fuzzification
def fuzzify(crisp_val, var_fsets):
    fuzzified = {}
    for term, mf in var_fsets.items():
        fuzzified[term] = mf(crisp_val)
    return fuzzified

# Step 2: Rule evaluation
def evaluate_rules(fuzzified_input):
    rules_strength = []
    for i, in_term in enumerate(input_terms):
        degree = fuzzified_input[in_term]
        if degree > 0:
            for j, out_term in enumerate(output_terms):
                if rule_base[i, j] == 1:
                    rules_strength.append((degree, out_term))
    return rules_strength

# Step 3: Aggregation
def aggregate(rules_strength, resolution=1000):
    x_vals = np.linspace(0, 1, resolution)
    agg = np.zeros(resolution)
    for strength, out_term in rules_strength:
        mf_vals = np.array([output_vars['fan_speed'][out_term](x) for x in x_vals])
        clipped = np.minimum(mf_vals, strength)
        agg = np.maximum(agg, clipped)
    return agg, x_vals

# Step 4: Defuzzification methods
def centroid_defuzz(x, mf):
    if mf.sum() == 0:
        return 0
    return (x * mf).sum() / mf.sum()

def mean_of_max_defuzz(x, mf):
    max_m = mf.max()
    if max_m == 0:
        return 0
    max_points = x[mf == max_m]
    return max_points.mean()

def max_membership_defuzz(x, mf):
    max_idx = np.argmax(mf)
    return x[max_idx]

# Main function combining steps
def mamdani_fis(crisp_input, defuzz_method='centroid'):
    fuzzified = fuzzify(crisp_input, input_vars['temperature'])
    rules_strength = evaluate_rules(fuzzified)
    agg_mf, x_vals = aggregate(rules_strength)

    if defuzz_method == 'centroid':
        return centroid_defuzz(x_vals, agg_mf)
    elif defuzz_method == 'mean_of_max':
        return mean_of_max_defuzz(x_vals, agg_mf)
    elif defuzz_method == 'max_membership':
        return max_membership_defuzz(x_vals, agg_mf)
    else:
        raise ValueError("Unknown defuzzification method")

# Example usage
input_val = 22
print("Centroid defuzz output:", mamdani_fis(input_val, 'centroid'))
print("Mean of max defuzz output:", mamdani_fis(input_val, 'mean_of_max'))
print("Max membership defuzz output:", mamdani_fis(input_val, 'max_membership'))
