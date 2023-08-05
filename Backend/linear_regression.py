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
    query = "SELECT strftime('%Y-%m-%d',Start) as Start, strftime('%Y-%m-%d',End) as End FROM periodlog WHERE id = {} ORDER BY Start".format(userid)
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


    # # Prediction one step ahead / new cycle
     #prediction_one_step_ahead = model_LR.predict([test_x[-1]])
    cycles_numbers = np.arange(1, len(cycle_length) + 1)
       # Calculate the predicted next cycle length


    last_predicted_cycle_length = cycle_length[0]
    last_predicted_cycle_length_2=cycle_length[0]+cycle_length[1]
    last_predicted_cycle_length_3=cycle_length[0]+cycle_length[1]+cycle_length[2]


     # Calculate the predicted next period start date
    last_period_end_date = datetime.strptime(df['End'].iloc[-1], '%Y-%m-%d')
    next_period_start_date = last_period_end_date + timedelta(days=last_predicted_cycle_length)
    last_period_start_date = datetime.strptime(df['Start'].iloc[-1], '%Y-%m-%d')
    next_period_start_date = last_period_start_date + timedelta(days=last_predicted_cycle_length)
    next_period_start_date_2=last_period_start_date + timedelta(days=last_predicted_cycle_length_2)
    next_period_start_date_3=last_period_start_date + timedelta(days=last_predicted_cycle_length_3)

     # Calculate the predicted next period end date
    next_period_end_date = next_period_start_date + timedelta(days=periods[-1])
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

     
    print("Predicted cycle-2 period start date:", formatted_next_period_start_date_2)
    print("Predicted cycle-2 period end date:", formatted_next_period_end_date_2)
    print("Predicted cycle-3 period start date:", formatted_next_period_start_date_3)
    print("Predicted cycle-3 period end date:", formatted_next_period_end_date_3) 
    
    # # Calculate the predicted next cycle length
    # last_predicted_cycle_length = cycle_length[-1]

    # # Calculate the predicted next period start date
    # last_period_end_date = datetime.strptime(df['End'].iloc[-1], '%Y-%m-%d')
    # next_period_start_date = last_period_end_date + timedelta(days=last_predicted_cycle_length)

    # # Calculate the predicted next period end date
    # next_period_end_date = next_period_start_date + timedelta(days=periods[-1])

    # # Format and print the results
    # formatted_next_period_start_date = next_period_start_date.strftime('%Y-%m-%d')
    # formatted_next_period_end_date = next_period_end_date.strftime('%Y-%m-%d')

    # print("Predicted next period start date:", formatted_next_period_start_date)
    # print("Predicted next period end date:", formatted_next_period_end_date)



    #Calculate irregularities
     # Get the current year
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    endyear = current_year

    print("Start Date?")
    daystart = input("Day: ")
    monthstart = input("Month: ")

    print("End Date?")
    dayend = input("Day: ")
    monthend = input("Month: ")

    if current_month == 12:
      endyear = int(input("End Year? "))"""
    
    
    #start <= end <= current 

    '''
    ActualDateSTART = f"{current_year}-0{current_month}-{daystart} "
    ActualDateEND = f"{end_year}-0{endmonth}-{dayend} "
    start_date = datetime.strptime(ActualDateSTART, "%Y-%m-%d ")
    '''
    # Define the format for the input dates
    input_format = "%Y-%m-%d"
    
    #try:
    # Parse the input dates using the specified format

    while(True):#CHANGE TO WHILE INPUT IS INVALID
        start_date =input('Enter start date: ')
        end_date = input('Enter end date: ')
        start_date= datetime.strptime(start_date, input_format).date()
        end_date = datetime.strptime(end_date, input_format).date()

        # Check if start date is smaller than end date
        if start_date <= end_date and end_date <= datetime.strptime(str(datetime.now().date()), input_format).date():
            print("Start date:", start_date)
            print("End date:", end_date)
            break
        else:
            #Display a message
            print("Start date should be smaller than end date.")


   
    ErrorvalINT = (abs(next_period_start_date.date() - start_date)).days
    print("Error Value:", ErrorvalINT)

    if ErrorvalINT < 10:
        new_row_data = {
        'start': str(start_date),
        'end': str(end_date)
        # Add more columns and their values as needed
        }
        add_new_row_to_table(new_row_data, 'periodLog', conn,2)

    # Optionally, you can print the new row DataFrame to check its contents
    
    else: #CHECK IF WORKS
        #QUESTIONS AND FORGOT?
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
                



'''
    except ValueError:
        print("Invalid date format. Please enter valid dates in yyyy-mm-dd format.")
    
    Errorval = abs(next_period_start_date.date() - start_date)
    ErrorvalINT = Errorval.total_seconds() / (60 * 60 * 24)
    print("Error Value:", ErrorvalINT)
'''

