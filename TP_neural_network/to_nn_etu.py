import numpy as np
from scipy import sparse
from sklearn import datasets
from sklearn.model_selection import train_test_split

class neural_network(object):
    def __init__(self,data,target,num_layer,input_size,output_size,num_epoch=100,lr=0.001,is_bias = False):
        self.num_layer = num_layer
        self.data = data.T
        self.data = (self.data - self.data.min())/(self.data.max() - self.data.min())
        self.lr = lr
        target = self.convert_labels(target,output_size)
        self.labels = target
        self.is_bias = is_bias
        self.num_epoch = num_epoch
        weight = []
        nb_neurons_prec = input_size
        biases = []
        for i in range(num_layer-1):
            nb_neurons = int(input('Number of neurones in layer'+str(i+1)+'?'))
            weight_i = np.random.randn(nb_neurons_prec,nb_neurons)
            if is_bias:
                bias = np.random.randn(nb_neurons,1)
                biases.append(bias)
                
            weight.append(weight_i)
            nb_neurons_prec = nb_neurons
        weight_last = np.random.randn(nb_neurons_prec,output_size)
        weight.append(weight_last)
        self.weights = weight
        self.biases = biases
        # Z = []
        # self.Z = Z

    def forward(self):
        self.Z=[]
        self.A=[]
        a=self.data
        self.A.append(a)
        for i in range(self.num_layer-1):
            #zl = self.weights[l] * self.data[l-1] + self.biases[l]
            if self.is_bias:
                z=np.dot(self.weights[i].T,a)+self.biases[i]
            else:
                z=np.dot(self.weights[i].T,a)
            a=np.maximum(z,0)  #relu
            self.Z.append(z)
            self.A.append(a)
        out = np.dot(self.weights[self.num_layer-1].T,a)
        self.out_softmax = self.softmax(out)
        
    def backward(self):
        self.E = []
        self.dW = []
        self.db = []
        e = (self.out_softmax - self.labels)/(self.labels.shape[1])
        dw = np.dot(self.A[-1],e.T)
        self.dW.append(dw)

        for i in range(self.num_layer-1):
            a = self.A[-i-2]
            z = self.Z[-i-1]
            e = np.dot(self.weights[-i-1], e)
            e[z<=0] = 0
            dw = np.dot(a,e.T)
            if self.is_bias:
                db = np.sum(e, axis=1, keepdims=True)
                self.db.append(db)
            self.dW.append(dw)

        for i in range(self.num_layer):
            self.weights[i] += -self.lr * self.dW[-i-1]

        if self.is_bias:
            for i in range(self.num_layer-1):
                self.biases[i] += -self.lr * self.db[-i-1]
        
    def learning(self):
        for epoch in range(self.num_epoch):
            self.forward()
            self.loss = self.cost(self.labels,self.out_softmax)
            print(self.loss)
            self.backward()

    # Softmax score    
    def softmax(self,V):
        e_V = np.exp(V - np.max(V, axis = 0, keepdims = True))
        Z = e_V / e_V.sum(axis = 0)
        return Z

    # One-hot coding
    def convert_labels(self,y,C = 3):
        Y = sparse.coo_matrix((np.ones_like(y),
            (y, np.arange(len(y)))), shape = (C, len(y))).toarray()
        return Y

    # cost or loss function
    def cost(self,Y,Yhat):
        return -np.sum(Y*np.log(Yhat))/Y.shape[1]

if __name__=="__main__":
    iris = datasets.load_iris()
    data = iris.data
    target = iris.target
    
    data_train,datat_test,target_train, target_test = train_test_split(data,target,test_size=0.2)
    
    nn = neural_network(data_train,target_train,5,4,3,is_bias=True)
    nn.learning()