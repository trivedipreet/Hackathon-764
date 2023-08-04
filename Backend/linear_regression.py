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
 with sqlite3.connect('BackendPeriodTracker.db') as conn:
    
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
    # Calculate the predicted next cycle length
    last_predicted_cycle_length = cycle_length[-1]

    # Calculate the predicted next period start date
    last_period_end_date = datetime.strptime(df['End'].iloc[-1], '%Y-%m-%d')
    next_period_start_date = last_period_end_date + timedelta(days=last_predicted_cycle_length)

    # Calculate the predicted next period end date
    next_period_end_date = next_period_start_date + timedelta(days=periods[-1])

    # Format and print the results
    formatted_next_period_start_date = next_period_start_date.strftime('%Y-%m-%d')
    formatted_next_period_end_date = next_period_end_date.strftime('%Y-%m-%d')

    print("Predicted next period start date:", formatted_next_period_start_date)
    print("Predicted next period end date:", formatted_next_period_end_date)


    '''
    plt.figure(figsize=(4, 4))
    plt.rcParams.update({'font.size': 16})

    plt.plot(cycle_length, '-->', color='blue')
    plt.plot(periods, '-*', color='green')
    plt.plot(test_y, ':o', color='red')
    plt.plot(cycles_numbers[-1], prediction_one_step_ahead[0][0], '-->', color='blue')
    plt.plot(cycles_numbers[-1], prediction_one_step_ahead[0][1], '-*', color='green')
    plt.legend(['Cycle Duration (Predicted)', 'Period Variation (Predicted)', 'Real Data'])
    plt.grid()
    plt.xlabel('Cycles')
    plt.ylabel('Days')
    plt.title('Linear Regression Model')
    fig = plt.gcf()
    #fig.savefig('Rujuta/linear.png', dpi=300, bbox_inches='tight')
    #plt.show()

    error = abs(test_y - y_pred)
    plt.plot(error[:, 0], '-->', color='blue')
    plt.plot(error[:, 1], '-*', color='green')
    plt.legend(['Cycle Error', 'Period Error'])
    plt.grid()
    plt.xlabel('Cycles')
    plt.ylabel('Days')
    plt.title('Linear Regression Model')
    fig = plt.gcf()
    #fig.savefig('Rujuta/linear_error.png', dpi=300, bbox_inches='tight')
    #plt.show()

    # Calculate RMSE (Root Mean Squared Error)
    rms = sqrt(mean_squared_error(test_y, y_pred))
    print('RMSE: ', rms)

    # Calculate MAE (Mean Absolute Error)
    mae = np.mean(np.abs((test_y - y_pred)))
    print('MAE: ', mae)'''


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

  






   