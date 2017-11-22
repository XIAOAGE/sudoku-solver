import pickle
import gzip
import random
import json
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

def load_data(filename="data/res/"):
    INPUT_W = 5
    INPUT_H = 5
    training_filedir_pre = filename
    training_data = []
    test_data = []
    for i in range(9):
        i = i+1
        print("Images for: ", i)
        training_filedir = training_filedir_pre + str(i) + "/*"
        for training_file in glob.glob(training_filedir):
            training_array = Image.open(training_file)
            training_array = training_array.resize((INPUT_W, INPUT_H), Image.ANTIALIAS)
            training_array = np.array(training_array)
            training_data.append((np.reshape(training_array, (INPUT_W*INPUT_H, 1)) / 255.0, vectorize(i)))
            test_data.append((np.reshape(training_array, (INPUT_W*INPUT_H, 1)) / 255.0, i))

    filename="data/30x20/Set"
    training_filedir_pre = filename + "1/"
    for i in range(10):
        training_filedir = training_filedir_pre + str(i) + "/*"
        for training_file in glob.glob(training_filedir):
            training_array = Image.open(training_file)
            training_array = training_array.resize((INPUT_W, INPUT_H), Image.ANTIALIAS)
            training_array = np.array(training_array)
            training_data.append((np.reshape(training_array, (INPUT_W*INPUT_H, 1)) / 255.0, vectorize(i)))

    filename="data/60x40/Set"
    training_filedir_pre = filename + "1/"
    for i in range(9):
        i = i+1
        training_filedir = training_filedir_pre + str(i) + "/*"
        for training_file in glob.glob(training_filedir):
            training_array = Image.open(training_file)
            training_array = training_array.resize((INPUT_W, INPUT_H), Image.ANTIALIAS)
            training_array = np.array(training_array)
            training_data.append((np.reshape(training_array, (INPUT_W*INPUT_H, 1)) / 255.0, vectorize(i)))
    
    filename="data/60x40/Set"
    training_filedir_pre = filename + "2/"
    for i in range(9):
        i = i+1
        training_filedir = training_filedir_pre + str(i) + "/*"
        for training_file in glob.glob(training_filedir):
            training_array = Image.open(training_file)
            training_array = training_array.resize((INPUT_W, INPUT_H), Image.ANTIALIAS)
            training_array = np.array(training_array)
            training_data.append((np.reshape(training_array, (INPUT_W*INPUT_H, 1)) / 255.0, vectorize(i)))

    test_filedir_pre = filename + "2/"
    test_data = []
    for i in range(9):
        i = i+1
        test_filedir = test_filedir_pre + str(i) + "/*"
        for test_file in glob.glob(test_filedir):
            test_array = Image.open(test_file)
            test_array = test_array.resize((INPUT_W, INPUT_H), Image.ANTIALIAS)
            test_array = np.array(test_array)
            test_data.append((np.reshape(test_array, (INPUT_W*INPUT_H, 1)) / 255.0, i))
            #training_data.append((np.reshape(test_array, (INPUT_W*INPUT_H, 1)) / 255.0, vectorize(i)))

    return (training_data, test_data)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z) * (1-sigmoid(z))

def vectorize(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

class QuadraticCost(object):
    
    @staticmethod
    def fn(a, y):
        return 0.5*np.linalg.norm(a-y)**2
    
    @staticmethod
    def delta(z, a, y):
        return (a-y) * sigmoid_prime(z)

class CrossEntropyCost(object):
    
    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))
    
    @staticmethod
    def delta(z, a, y):
        return (a-y)

class Network(object):

    def __init__(self, sizes, cost=CrossEntropyCost):
        self.size = len(sizes)
        self.layers = sizes
        self.default_weight_initializer()
        self.cost=cost
        
    def default_weight_initializer(self):
        self.bias = [np.random.randn(y, 1) for y in self.layers[1:]]
        self.weight = [np.random.randn(y, x)/np.sqrt(x)
                       for x, y in zip(self.layers[:-1], self.layers[1:])]

    def large_weight_initializer(self):
        self.bias = [np.random.randn(y, 1) for y in self.layers[1:]]
        self.weight = [np.random.randn(y, x)
                       for x, y in zip(self.layers[:-1], self.layers[1:])]
        
    def feedforward(self, a):
        for b, w in zip(self.bias, self.weight):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda = 0.0, test_data=None):
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size]
                            for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                mini_batch = list(zip(*mini_batch))
                mini_batch_x = np.column_stack(mini_batch[0])
                mini_batch_y = np.column_stack(mini_batch[1])
                self.update_mini_batch((mini_batch_x, mini_batch_y), eta, lmbda, n)
            print("Epoch: ",j+1," - ",str(self.evaluate(test_data))+" / "+str(len(test_data)))


    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        mini_batch_x = mini_batch[0]
        mini_batch_y = mini_batch[1]
       
        gradient_w, gradient_b = self.backprop(mini_batch_x, mini_batch_y)
        self.weight = [(1-eta*(lmbda/n))*w-eta*nw
                        for w, nw in zip(self.weight, gradient_w)]
        self.bias = [b-eta*nb
                        for b, nb in zip(self.bias, gradient_b)]

    def backprop(self, x, y):
        gradient_w = [np.zeros(w.shape) for w in self.weight]
        gradient_b = [np.zeros(b.shape) for b in self.bias]
        batch_size = len(x[0])
        activations = [x]
        zs = []
        for w, b in zip(self.weight, self.bias):
            z = np.dot(w, x) + b
            zs.append(z)
            x = sigmoid(z)
            activations.append(x)

        deltaL = (self.cost).delta(zs[-1], x, y)
        gradient_b[-1] = np.sum(deltaL, axis=1, keepdims=True) * 1.0 / batch_size
        tmp_gradient_w = np.dot(deltaL, activations[-2].transpose())
        gradient_w[-1] = tmp_gradient_w * 1.0 / batch_size

        for l in range(2, self.size):
            deltaL = np.dot(self.weight[-l+1].transpose(), deltaL) * sigmoid_prime(zs[-l])
            gradient_b[-l] = np.sum(deltaL, axis=1, keepdims=True) * 1.0 / batch_size
            tmp_gradient_w = np.dot(deltaL, activations[-l-1].transpose())
            gradient_w[-l] =  tmp_gradient_w * 1.0 / batch_size

        return (gradient_w, gradient_b)

    def predict(self, input_data):
        result = np.argmax(self.feedforward(input_data))
        #result = self.feedforward(input_data)
        return result

    def evaluate(self, test_data):
        result = [(np.argmax(self.feedforward(x)), y)
                    for x, y in test_data]
        # print(result)
        return sum(int(x == y) for x, y in result)
    
    def save(self, filename):
        data = {"layers": self.layers,
                "weight": [w.tolist() for w in self.weight],
                "bias": [b.tolist() for b in self.bias],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()

def load(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["layers"], cost=cost)
    net.weight = [np.array(w) for w in data["weight"]]
    net.bias = [np.array(b) for b in data["bias"]]
    return net