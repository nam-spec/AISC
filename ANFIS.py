import numpy as np

# ---------------------------
# 1. Membership Functions
# ---------------------------
def gauss_mf(x, c, sigma):
    """Gaussian membership function"""
    return np.exp(-0.5 * ((x - c) / sigma)**2)

# ---------------------------
# 2. Example Input Data
# ---------------------------
# Let's assume 1 input feature for simplicity
X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 3, 2.5, 4, 5])  # Target outputs

# ---------------------------
# 3. Fuzzy Rules (2 rules for example)
# ---------------------------
# Each rule has a Gaussian MF with center c and width sigma
rule_params = [
    {'c': 2.0, 'sigma': 1.0, 'p': 0.5, 'q': 1.0, 'r': 0.2},  # Rule 1: output = p*x + q
    {'c': 4.0, 'sigma': 1.0, 'p': 1.0, 'q': 0.5, 'r': 0.1}   # Rule 2
]

# ---------------------------
# 4. Training Loop (Forward Pass)
# ---------------------------
learning_rate = 0.01
epochs = 50

for epoch in range(epochs):
    total_error = 0
    for x, y_true in zip(X, Y):
        # Step 1: Compute membership values for each rule
        w = np.array([gauss_mf(x, r['c'], r['sigma']) for r in rule_params])
        
        # Step 2: Normalize firing strengths
        w_sum = np.sum(w)
        w_norm = w / w_sum
        
        # Step 3: Compute rule outputs (linear functions)
        f = np.array([r['p']*x + r['q'] for r in rule_params])
        
        # Step 4: Compute overall ANFIS output
        y_pred = np.sum(w_norm * f)
        
        # Step 5: Compute error
        error = y_true - y_pred
        total_error += error**2
        
        # Step 6: Update consequent parameters (p, q) using simple gradient descent
        for i, r in enumerate(rule_params):
            r['p'] += learning_rate * error * w_norm[i] * x
            r['q'] += learning_rate * error * w_norm[i]
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, MSE: {total_error/len(X):.4f}")

# ---------------------------
# 5. Test ANFIS
# ---------------------------
print("\nPredictions:")
for x in X:
    w = np.array([gauss_mf(x, r['c'], r['sigma']) for r in rule_params])
    w_norm = w / np.sum(w)
    f = np.array([r['p']*x + r['q'] for r in rule_params])
    y_pred = np.sum(w_norm * f)
    print(f"x={x}, y_pred={y_pred:.2f}")
