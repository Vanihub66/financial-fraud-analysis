
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect Python to MySQL
password = input("Enter your MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="fraud_analysis"
)

print("\nMySQL connected successfully!")

# 2. Create a folder to save graphs
os.makedirs("charts", exist_ok=True)


# Helper function: run SQL and return results as a DataFrame
def run_query(query):
    cursor = connection.cursor()
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    cursor.close()

    return pd.DataFrame(rows, columns=columns)


# 3. Fraud vs Normal Transactions
query1 = """
SELECT
    isFraud,
    COUNT(*) AS total_transactions,
    ROUND(AVG(amount), 2) AS average_amount
FROM fraud_transactions
GROUP BY isFraud
"""

df1 = run_query(query1)

print("\n--- 1. Fraud vs Normal Transactions ---")
print(df1.to_string(index=False))

labels = [
    "Normal-labelled" if value == 0 else "Fraud-labelled"
    for value in df1["isFraud"]
]

plt.figure(figsize=(8, 5))
plt.bar(labels, df1["average_amount"])
plt.title("Average Transaction Amount")
plt.xlabel("Transaction Category")
plt.ylabel("Average Amount")
plt.ticklabel_format(axis="y", style="plain")
plt.tight_layout()
plt.savefig("charts/average_transaction_amount.png", dpi=150)
plt.close()


# 4. Transaction Distribution
query2 = """
SELECT
    isFraud,
    COUNT(*) AS total_transactions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM fraud_transactions),
        4
    ) AS transaction_percentage
FROM fraud_transactions
GROUP BY isFraud
"""

df2 = run_query(query2)

print("\n--- 2. Transaction Distribution ---")
print(df2.to_string(index=False))

labels = [
    "Normal-labelled" if value == 0 else "Fraud-labelled"
    for value in df2["isFraud"]
]

plt.figure(figsize=(8, 5))
plt.bar(labels, df2["transaction_percentage"])
plt.title("Transaction Distribution")
plt.xlabel("Transaction Category")
plt.ylabel("Percentage of All Transactions")
plt.tight_layout()
plt.savefig("charts/transaction_distribution.png", dpi=150)
plt.close()


# 5. Fraud Rate by Transaction Type
query3 = """
SELECT
    type,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(
        SUM(isFraud) * 100.0 / COUNT(*),
        4
    ) AS fraud_rate_percentage
FROM fraud_transactions
GROUP BY type
ORDER BY fraud_rate_percentage DESC
"""

df3 = run_query(query3)

print("\n--- 3. Fraud Rate by Transaction Type ---")
print(df3.to_string(index=False))

plt.figure(figsize=(9, 5))
plt.bar(df3["type"], df3["fraud_rate_percentage"])
plt.title("Fraud-labelled Transaction Rate by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Fraud Rate (%)")
plt.tight_layout()
plt.savefig("charts/fraud_rate_by_type.png", dpi=150)
plt.close()


# 6. High-Value vs Other Transactions
query4 = """
SELECT
    CASE
        WHEN amount >= 1000000 THEN 'High Value'
        ELSE 'Other Transactions'
    END AS transaction_category,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(
        SUM(isFraud) * 100.0 / COUNT(*),
        4
    ) AS fraud_rate_percentage,
    ROUND(AVG(amount), 2) AS average_amount
FROM fraud_transactions
GROUP BY
    CASE
        WHEN amount >= 1000000 THEN 'High Value'
        ELSE 'Other Transactions'
    END
"""

df4 = run_query(query4)

print("\n--- 4. High-Value Transaction Analysis ---")
print(df4.to_string(index=False))

plt.figure(figsize=(8, 5))
plt.bar(df4["transaction_category"], df4["fraud_rate_percentage"])
plt.title("Fraud-labelled Rate: High-Value vs Other Transactions")
plt.xlabel("Transaction Category")
plt.ylabel("Fraud Rate (%)")
plt.tight_layout()
plt.savefig("charts/high_value_transaction_analysis.png", dpi=150)
plt.close()


# 7. Finish
connection.close()

print("\nAnalysis completed successfully!")
print("All four graphs have been saved in the charts folder.")
