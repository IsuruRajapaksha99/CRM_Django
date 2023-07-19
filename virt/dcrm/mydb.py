import mysql.connector

dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "messi1234",

)

#prepare a cursor object using cursor() method
cursorObject = dataBase.cursor()

#Create Database
cursorObject.execute("CREATE DATABASE CRMDB")

print("Database Created Successfully")