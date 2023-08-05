# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

# Importing the dataset
dataset = pd.read_csv('Backend\PCOS.csv')
x = dataset.iloc[:, :-1].values #all columns except the last
y = dataset.iloc[:, -1].values #last column

# Splitting the dataset into the Training set and Test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state = 0)

'''
print(x_train)
print(y_train)
print(x_test)
print(y_test)
'''

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

'''
print(x_train)
print(x_test)
'''

# Training the Logistic Regression model on the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(x_train, y_train)
'''
# Predicting the Test set results
y_pred = classifier.predict(x_test)
print(y_pred)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))
'''

# Predicting a new result
#age, weight, height, cycle(r/i), cycle length, #abortions, pregnant, weight gain, hair growth,skin darkening, hair loss, pimples, fast food, exercise
print(classifier.predict(sc.transform([[21,50,155,4,9,0,0,1,0,1,1,1,1,0]])))

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)