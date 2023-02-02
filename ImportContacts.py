import pandas as pd
import re
import mysql.connector
import os

CallerIDdata = pd.read_csv(r'/home/user/Downloads/contacts.csv')
dbConnection = mysql.connector.connect(host='192.168.X.X', database='CallerID', user='user', password='password')
dbCursor = dbConnection.cursor()
dbCursor.execute("truncate table tblCallerID;")

def CheckRecord(Name,Number,Type):
    Number = str(Number)
    if Number != 'nan':
        Name = str(Name).replace("'","''")
        Number = re.sub("[^0-9]", "", Number)
        if len(Number) != 11:
            if len(Number) == 10:
                Number = '1'+Number
            else:
                print(f"{Name} {Number} {Type}")
        if len(Number) == 11:
            insertSQL = f"INSERT INTO tblCallerID (Name,Number,Type) VALUES ('{Name}','{Number}','{Type}');"
            dbCursor.execute(insertSQL)

for index, CallerID in CallerIDdata.iterrows():
    CheckRecord(CallerID["Name"],CallerID["Phone 1 - Value"],CallerID["Phone 1 - Type"])
    CheckRecord(CallerID["Name"],CallerID["Phone 2 - Value"],CallerID["Phone 2 - Type"])
    CheckRecord(CallerID["Name"],CallerID["Phone 3 - Value"],CallerID["Phone 3 - Type"])
    CheckRecord(CallerID["Name"],CallerID["Phone 4 - Value"],CallerID["Phone 4 - Type"])

dbCursor.execute("DELETE FROM tblAnveoSearch WHERE Number in (SELECT Number FROM tblCallerID);")

dbConnection.commit()
dbConnection.close()

os.remove('/home/user/Downloads/contacts.csv')