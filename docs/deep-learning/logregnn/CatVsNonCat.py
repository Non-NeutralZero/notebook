import os
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

train_file = h5py.File('/content/train_catvnoncat.h5', 'r')
test_file = h5py.File('/content/test_catvnoncat.h5', 'r')

for key in train_file.keys():
    print(key, end = ', ')

X_train = np.array(train_file['train_set_x'][:])
y_train = np.array(train_file['train_set_y'][:])

X_test = np.array(test_file['test_set_x'][:])
y_test = np.array(test_file['test_set_y'][:])

classes = np.array(test_file["list_classes"][:])

print(X_train.shape)
print(X_test.shape)

print(y_train.shape)
print(y_test.shape)

y_train = y_train.reshape((1, y_train.shape[0]))
y_test = y_test.reshape((1,y_test.shape[0]))
print(y_train.shape)
print(y_test.shape)

index = 0
plt.imshow(X_train[index])
str(y_train[:, index])

## Processing #1 : Reshaping X
X_train_p1 = X_train.reshape(X_train.shape[0],-1).T
X_test_p1 = X_test.reshape(X_test.shape[0],-1).T

print(X_train_p1.shape)
print(X_test_p1.shape)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def get_cost(X,w,b,Y):
  ### Forward Pass
  m = X.shape[1]
  Z = np.dot(w.T, X) + b

  ### Activation
  A = sigmoid(Z)

  ### Return Cost
  return np.sum(((- np.log(A))*Y + (-np.log(1-A))*(1-Y)))/m

def get_gradients(X,w,b,Y):
  m = X.shape[1]
  Z = np.dot(w.T, X) + b
  A = sigmoid(Z)

  dw = (np.dot(X, (A-Y).T))/m
  db = (np.sum(A - Y, axis=1, keepdims=True)) / m
  return dw, db

## Backward Pass
def optimizer(X,w,b,Y,learningrate, iterations):
  costs=[]

  for i in range(iterations):
    dw, db = get_gradients(X,w,b,Y)
    w = w - (learningrate*dw)
    b = b - (learningrate*db)

    cost = get_cost(X,w,b,Y)
    costs.append(cost)

  return dw, db, w, b, costs

def get_predictions(X,w,b,baseline=0.5):
  m = X.shape[1]
  y_pred = np.zeros((1, m))
  A = sigmoid(np.dot(w.T,X) + b)

  for i in range(A.shape[1]):
      if A[0, i] >= baseline:
          y_pred[0, i] = 1
      else:
          y_pred[0, i] = 0

  return y_pred


size_w = X_train_p1.shape[0]
w = np.zeros((size_w, 1))
b = 0

## Experiment: try different learningrates
dw, db, w, b, costs = optimizer(X_train_p1, w, b, y_train, learningrate=0.00001, iterations= 50)
dw, db, w, b, costs

size_w = X_train_p1.shape[0]
w = np.zeros((size_w, 1))
b = 0

## Experiment: try different learningrates and iterations
dw, db, w, b, costs = optimizer(X_train_p1, w, b, y_train, learningrate=0.001, iterations= 50)
dw, db, w, b, costs

def train(X_train, X_test, y_train, y_test, learningrate, iterations):

  ## Init parameters
  size_w = X_train.shape[0]
  w = np.zeros((size_w, 1))
  b = 0

  ## Optimize
  dw, db, w, b, costs = optimizer(X_train, w, b, y_train, learningrate, iterations)

  ## Predict
  y_pred_train = get_predictions(X_train,w,b,baseline=0.5)
  y_pred_test = get_predictions(X_test,w,b,baseline=0.5)

  train_accuracy = 100 - round(np.mean(np.abs(y_pred_train - y_train)) * 100, 3)
  test_accuracy = 100 - round(np.mean(np.abs(y_pred_test - y_test)) * 100, 3)

  print(f"Training accuracy: {train_accuracy} %")
  print(f"Test accuracy: {test_accuracy} %")

  predictions = {
        "training_predictions" : y_pred_train,
        "test_predictions" : y_pred_test,
    }

  return predictions, costs

predictions, costs = train(X_train_p1, X_test_p1, y_train, y_test, learningrate=0.0000001, iterations= 50)

iterations= 50
plt.plot(range(0, iterations), costs)
