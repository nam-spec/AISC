import numpy as np

def activation(ans):
    if(ans>=0):
        return 1
    else:
        return 0



def test(X,w,b):
    for i in range(len(X)):
        print(X[i][0],' : ', X[i][1], ' = ', activation(np.dot(w,X[i])+b))



def train(X,Y,lr=1,epochs=20):
    w=[0,0]
    b=0
    
    for _ in range(epochs):
        for i in range(len(X)):
            y_got=activation(np.dot(w,X[i])+b)
            error=Y[i]-y_got
            w=w+lr*error*X[i]
            b=b+lr*error
            
    return w,b



X=np.array([[0,0],[0,1],[1,0],[1,1]])
Y=np.array([0,0,0,1])
w,b=train(X,Y,epochs=10)
print('weights: ',w, ' bias: ', b)
test(X,w,b)
