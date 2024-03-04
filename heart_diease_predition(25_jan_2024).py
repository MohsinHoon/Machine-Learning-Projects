# -*- coding: utf-8 -*-
"""Heart Diease Predition(25 Jan 2024)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tMGj57ga6Pfo6plzESaeVDws43cDazO_
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Drive **Mounting**

** Mohsin Ali **

---
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

"""Reading The CSV using Pandas"""

heart=pd.read_csv('/content/drive/MyDrive/heart.csv')
heart.head()

heart.tail()

heart.info()

"""Plotting Graph for Head First 5 Values"""

plt.plot(heart.head())
plt.show

"""Plotting Grapgh for Tail Last 5 Values"""

plt.plot(heart.tail())
plt.show

"""**Checking Null Values**"""

# checking for missing values
heart.isnull().sum()

"""**Description of Cell**"""

# statistical measures about the data
heart.describe()

"""**Disturbution of Cells Accordingly**"""

# checking the distribution of Target Variable
heart['target'].value_counts()

"""**Dropping Coloumn and Axis**"""

X = heart.drop(columns='target', axis=1)
Y = heart['target']

"""**Printing X**"""

print(X)

"""Printing Y"""

print(Y)

"""**Splitting Into Testing and Training Data**"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3,train_size=0.7, stratify=Y,random_state=2)

"""**Printing X and Y shapes**"""

print(X.shape, X_train.shape, X_test.shape)

"""# ** Naive Bayes Algorithm**

"""

nb_model = GaussianNB()
nb_model.fit(X_train, Y_train)
nb_predictions = nb_model.predict(X_test)

"""**Training Data Accuracy**"""

#Predictions on the training set
train_predictions = nb_model.predict(X_train)

# Calculate training accuracy
train_accuracy = accuracy_score(Y_train, train_predictions)

print("Training Accuracy:", train_accuracy)

print("Naive Bayes Accuracy:", accuracy_score(Y_test, nb_predictions))
print("Naive Bayes Classification Report:")
print(classification_report(Y_test, nb_predictions))

"""**ROC Curve**

Standard Scaler is basically used for normalize the features of dataset
"""

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""As, we have applied the Naives bayes algortihm so we have added Guassian NB"""

model = GaussianNB()
model.fit(X_train, Y_train)

"""In this case we will get the result in One dimensional Array"""

y_prob = model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(Y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""**LSTM**"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""0= Number of Samples in Training Set
1= Number of Features in Sample
1 denoted as dimension
"""

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

"""50 Memory unit for pre-processing sequental data"""

# Build LSTM model
model = Sequential()
model.add(LSTM(50, input_shape=(X_train.shape[1], 1)))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam' ,metrics=['accuracy'])

Heart=model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_split=0.2)

y_pred_probabilities = model.predict(X_test)
# Assuming your model outputs probabilities for binary classification

# Applying a threshold of 0.5 to get binary predictions
y_pred = (y_pred_probabilities>0.5 )#.astype("int32")

test_accuracy = accuracy_score(Y_test, y_pred)
print(f'Test Accuracy: {test_accuracy:.2f}')

#activation='sigmoid')