import numpy as np

class MLP:
    def __init__(self, input_size, hidden_size, output_size, lr=0.1):
        self.lr = lr
        self.W1 = np.random.uniform(-1, 1, (hidden_size, input_size))
        self.b1 = np.zeros((hidden_size, 1))
        self.W2 = np.random.uniform(-1, 1, (output_size, hidden_size))
        self.b2 = np.zeros((output_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, x):
        self.x = x
        self.z1 = self.W1 @ x + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = self.W2 @ self.a1 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, target):
        output_error = target - self.a2  # Output layer error
        d_output = output_error * self.sigmoid_derivative(self.a2)

        hidden_error = self.W2.T @ d_output
        d_hidden = hidden_error * self.sigmoid_derivative(self.a1)
 
        # Update weights
        self.W2 += self.lr * d_output @ self.a1.T
        self.b2 += self.lr * d_output

        self.W1 += self.lr * d_hidden @ self.x.T
        self.b1 += self.lr * d_hidden

    def train(self, X, y, epochs=10000):
        for _ in range(epochs):
            for i in range(len(X)):
                x = X[i].reshape(2,1)
                target = y[i].reshape(1,1)
                self.forward(x)
                self.backward(target)


# Training XOR
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

mlp = MLP(input_size=2, hidden_size=2, output_size=1)
mlp.train(X, y)

# Predictions
for i in range(4):
    print(X[i], " -> ", mlp.forward(X[i].reshape(2,1)))
