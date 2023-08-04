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
from operations import add_new_row_to_table



def PREDICT():
 with sqlite3.connect('Backend\PeriodTracker.db') as conn:
    
    #conn = sqlite3.connect('PeriodTracker.db') #database path
    cur = conn.cursor()
    userid = 1
    query = "SELECT strftime('%Y-%m-%d',Start) as Start, strftime('%Y-%m-%d',End) as End FROM periodlog WHERE id = {}".format(userid)
    df = pd.read_sql_query(query, conn)
    #print(df)
    # Prepare data for linear regression/machine learning model
    
    periods_data = utils.calculate_datatime(df)
    #print(periods_data)
    
    features, labels = utils.generate_final_features(df)
    #print(features)
    #print(labels)

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=10)
    # Reshape data for linear regression/machine learning model
    train_y = np.array(y_train)
    train_x = np.array(x_train)
    test_x = np.array(x_test)
    test_y = np.array(y_test)
    train_x = train_x.reshape((train_x.shape[0], train_x.shape[1] * train_x.shape[2]))
    train_y = train_y.reshape((train_y.shape[0], train_y.shape[1] * 1))
    test_x = test_x.reshape((test_x.shape[0], test_x.shape[1] * test_x.shape[2]))
    test_y = test_y.reshape((test_y.shape[0], test_y.shape[1] * 1))

    # Linear regression model
    model_LR = LinearRegression()
    model_LR.fit(train_x, train_y)
    # Make predictions
    y_pred = model_LR.predict(test_x)
    output_pred = [[int(round(i[0])), int(round(i[1]))] for i in y_pred] # round the values 

    cycle_length = []
    periods = []
    for i in range(len(output_pred)):
        cycle_length.append(output_pred[i][0])
        periods.append(output_pred[i][1])


    # Prediction one step ahead / new cycle
    prediction_one_step_ahead = model_LR.predict([test_x[-1]])
    cycles_numbers = np.arange(1, len(cycle_length) + 1)

    last_predicted_cycle_length = cycle_length[0]
    last_predicted_cycle_length_2=cycle_length[0]+cycle_length[1]
    last_predicted_cycle_length_3=cycle_length[0]+cycle_length[1]+cycle_length[2]


    # Calculate the predicted next period start date
    last_period_start_date = datetime.strptime(df['Start'].iloc[-1], '%Y-%m-%d')
    next_period_start_date = last_period_start_date + timedelta(days=last_predicted_cycle_length)
    next_period_start_date_2=last_period_start_date + timedelta(days=last_predicted_cycle_length_2)
    next_period_start_date_3=last_period_start_date + timedelta(days=last_predicted_cycle_length_3)

    # Calculate the predicted next period end date
    next_period_end_date = next_period_start_date + timedelta(days=periods[0])
    next_period_end_date_2 = next_period_start_date_2 + timedelta(days=periods[1])
    next_period_end_date_3 = next_period_start_date_3 + timedelta(days=periods[2])


    # Format and print the results
    formatted_next_period_start_date = next_period_start_date.strftime('%Y-%m-%d')
    formatted_next_period_end_date = next_period_end_date.strftime('%Y-%m-%d')
    formatted_next_period_start_date_2 = next_period_start_date_2.strftime('%Y-%m-%d')
    formatted_next_period_end_date_2 = next_period_end_date_2.strftime('%Y-%m-%d')
    formatted_next_period_start_date_3 = next_period_start_date_3.strftime('%Y-%m-%d')
    formatted_next_period_end_date_3 = next_period_end_date_3.strftime('%Y-%m-%d')

    print("Predicted next period start date:", formatted_next_period_start_date)
    print("Predicted next period end date:", formatted_next_period_end_date)
    
    #Calculate irregularities
    print("Actual Date?")
    day = input("Day: ")
    month = int(input("Month: "))
    year = input("Year: ")
    ActualDate = f"{year}-{month}-{day} 00:00:00"
    actual_date_obj = datetime.strptime(ActualDate, "%Y-%m-%d %H:%M:%S")

    Errorval = abs(next_period_start_date - actual_date_obj)

    print("Error Value:", Errorval)

    new_row_data = {
     'start': actual_date_obj,
     'end': '2020-10-09'
     # Add more columns and their values as needed
     }
    add_new_row_to_table(new_row_data, 'periodLog', conn,2)

    # Optionally, you can print the new row DataFrame to check its contents   
    print("Predicted cycle-2 period start date:", formatted_next_period_start_date_2)
    print("Predicted cycle-2 period end date:", formatted_next_period_end_date_2)
    print("Predicted cycle-3 period start date:", formatted_next_period_start_date_3)
    print("Predicted cycle-3 period end date:", formatted_next_period_end_date_3)
    
    
    def lateperiod(forgottoenter):
       
       if forgottoenter:
         current_date = datetime.now().date()
         predstart1 = datetime.strptime(formatted_next_period_start_date, "%Y-%m-%d").date()
         predstart2 = datetime.strptime(formatted_next_period_start_date_2, "%Y-%m-%d").date()
         predstart3 = datetime.strptime(formatted_next_period_start_date_3, "%Y-%m-%d").date()
        
         if predstart1 < current_date:
                 d1 = {'start': formatted_next_period_start_date,
                    'end': formatted_next_period_end_date}
                 add_new_row_to_table(d1, 'periodLog', conn,2)
         if predstart2 < current_date:
                 d2 = {'start': formatted_next_period_start_date_2,
                    'end': formatted_next_period_end_date_2 }
                 add_new_row_to_table(d2, 'periodLog', conn,2)
         if predstart3 < current_date:
                 d3 = {'start': formatted_next_period_start_date_3,
                    'end': formatted_next_period_end_date_3 }
                 add_new_row_to_table(d3, 'periodLog', conn,2)
             
             





   
        
        
        