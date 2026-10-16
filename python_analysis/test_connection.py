
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter your MySQL password: "),
    database="fraud_analysis"
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM fraud_transactions")

total_rows = cursor.fetchone()[0]

print("Total transactions:", total_rows)

cursor.close()
connection.close()
