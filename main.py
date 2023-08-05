import utils
import numpy as np # For working with arrays
import pandas as pd
import matplotlib.pyplot as plt # For plotting graphs
from sklearn.linear_model import LinearRegression # To import the linear regression model
from sklearn.model_selection import train_test_split # To split the dataset into training and testing sets
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import datetime, timedelta
import sqlite3
from linear_regression import PREDICT

A,b,c = PREDICT('2022-08-08','2022-08-10',1)

print(c)