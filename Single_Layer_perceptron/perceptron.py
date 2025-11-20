import numpy as np

class Perceptron:
    def __init__(self,lr,epochs):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = 0

    def activation(self,x):
        if(x>=0) :
            return 1
        return 0
    
    def train(self,X,y):

        self.w = np.zeros(X.shape[1])

        for _ in range(self.epochs):
            for xi,target in zip(X,y):
                x = np.dot(xi,self.w) + self.b

                output = self.activation(x)

                error = target-output

                self.w += self.lr * error * xi
                self.b += self.lr * error

    def predict(self,X):
        outputs=[]
        for xi in X :
            net = np.dot(xi,self.w) + self.b
            outputs.append(self.activation(net))
        return outputs
        

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0,1,1,1])

p = Perceptron(0.1,10)

p.train(X,y)

print(f"weights : {p.w}")
print(f"bias : {p.b}")
print(f"Prediction : {p.predict(X)}")

