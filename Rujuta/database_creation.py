import sqlite3
import pandas as pd
import openpyxl

#try:
conn = sqlite3.connect('Rujuta/PeriodTracker.db') #database path
cur = conn.cursor()

#create tables:
cur.execute("""CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INT,
        gender CHAR(1),
        region TEXT,
        email TEXT NOT NULL,
        password TEXT NOT NULL);""")
cur.execute("""CREATE TABLE IF NOT EXISTS periodLog(id INTEGER REFERENCES user(id), 
        start DATE,
        end DATE)""")

'''
#run these commented commands ONLY ONCE
cur.execute("""INSERT INTO user(name, age, gender, region, email, password) VALUES("User1", 20, 'F', "Pune", "test", "test")""")
cur.execute("""INSERT INTO user(name, age, gender, region, email, password) VALUES("User2", 21, 'F', "Pune", "test2", "test2")""")


#excel to sql:
periodData = pd.read_excel('Rujuta/SyntheticData.xlsx', header=0)  
periodData.to_sql('periodLog', conn, if_exists='append', index=False)
periodData = pd.read_excel('Rujuta/RegularCycle.xlsx', header=0)  
periodData.to_sql('periodLog', conn, if_exists='append', index=False)
'''

conn.commit()

#except:
#    print("Unable to connect to database")
