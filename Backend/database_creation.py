import sqlite3
import pandas as pd
import openpyxl

#try:
conn = sqlite3.connect('Backend\PeriodTracker.db') #database path
cur = conn.cursor()

#create tables:

cur.execute("""CREATE TABLE IF NOT EXISTS regionInfo(Name TEXT PRIMARY KEY,
    Status	TEXT,
    District	TEXT,
    Population	TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INT,
        gender CHAR(1),
        region TEXT REFERENCES regionInfo(name),
        email TEXT NOT NULL,
        password TEXT NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS periodLog(id INTEGER REFERENCES user(id), 
        start TEXT,
        end TEXT)""")

#Adding data to the tables:
'''
periodData = pd.read_excel('Backend\SyntheticData.xlsx', header=0)  
periodData.to_sql('periodLog', conn, if_exists='append', index=False)
periodData = pd.read_excel('Backend\RegularCycle.xlsx', header=0)  
periodData.to_sql('periodLog', conn, if_exists='append', index=False)
regionData = pd.read_csv('Backend\Population.csv', header=0)  
regionData.to_sql('regionInfo', conn, if_exists='append', index=False)
'''


conn.commit()

#except:
#    print("Unable to connect to database")
