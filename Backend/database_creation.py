import sqlite3
import pandas as pd
import openpyxl
import random

#try:
conn = sqlite3.connect('Backend\PeriodTracker.db') #database path
cur = conn.cursor()

#create tables:

cur.execute("""CREATE TABLE IF NOT EXISTS regionInfo(Name TEXT PRIMARY KEY,
    Status	TEXT,
    District	TEXT,
    Population	TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS user (id TEXT(5) PRIMARY KEY,
        name TEXT NOT NULL,
        age INT,
        gender CHAR(1),
        region TEXT REFERENCES regionInfo(name),
        contact INT,
        password TEXT NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS doctor(id TEXT(5) PRIMARY KEY,
        name TEXT NOT NULL,
        qualification TEXT,
        reg_no INT,
        age INT, 
        gender CHAR(1),
        region TEXT REFERENCES regionInfo(name),
        contact INT,
        password TEXT NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS ngo(id TEXT(5) PRIMARY KEY,
        name TEXT NOT NULL,
        reg_no INT,
        region TEXT REFERENCES regionInfo(name),
        contact INT,
        password TEXT NOT NULL);""")

cur.execute("""CREATE TABLE IF NOT EXISTS periodLog(id TEXT(5) REFERENCES user(id), 
        start TEXT,
        end TEXT)""")

#userid generation
uid = "U"+str(random.randint(1000,9999))
uid2 = "U"+str(random.randint(1000,9999))

did = "D"+str(random.randint(1000,9999))
nid = "N"+str(random.randint(1000,9999))

#Adding data to the tables:
'''
cur.execute("""INSERT INTO user(id, name, age, gender, region, contact, password) VALUES(?,"User1", 20, 'F', "Pune", 1234567890, "password")""", (uid,))
cur.execute("""INSERT INTO user(id, name, age, gender, region, contact, password) VALUES(?, "User2", 21, 'F', "Pune", 678904321, "password")""",(uid2,))

cur.execute("""INSERT INTO doctor(id, name, qualification, reg_no, age, gender, region, contact, password) VALUES(?, "Doctor 1","MD Gyn", 12345, 41, 'F', "Pune", 904328761, "password")""",(did,))
cur.execute("""INSERT INTO ngo(id, name, reg_no, region, contact, password) VALUES(?,"NGO 1", 54321, "Pune", 7891234560, "password")""", (nid,))

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
