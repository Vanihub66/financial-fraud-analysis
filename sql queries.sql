-- Query 01:create Data base 

CREATE database fraud_analysis;
USE fraud_analysis;

CREATE TABLE fraud_transactions (
    step INT,
    type VARCHAR(20),
    amount DECIMAL(20,2),
    nameOrig VARCHAR(30),
    oldbalanceOrg DECIMAL(20,2),
    newbalanceOrig DECIMAL(20,2),
    nameDest VARCHAR(30),
    oldbalanceDest DECIMAL(20,2),
    newbalanceDest DECIMAL(20,2),
    isFraud TINYINT,
    isFlaggedFraud TINYINT
);
SHOW tables;
DESCRIBE fraud_transactions;

-- Query 02:set permissions 

SHOW VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = 1;
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Query 03:put the table in it 

USE fraud_analysis;
TRUNCATE TABLE fraud_transactions;

SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Query 04:Count fraud vs normal transactions

USE fraud_analysis;
SELECT
    isFraud,
    COUNT(*) AS total_transactions
FROM fraud_transactions
GROUP BY isFraud;

-- query 05:transaction type
USE fraud_analysis ;
SELECT 
type,
COUNT(*) AS total_transactions,
SUM(isFraud) AS Fraud_transactions,
ROUND( COUNT(*)*100.0/(SELECT COUNT(*) FROM fraud_transactions), 4) AS Fraud_percentage
FROM fraud_transactions
GROUP BY type
ORDER BY Fraud_transactions DESC ;

-- Query 6: Analyze amounts of fraud-labelled transactions

SELECT
    COUNT(*) AS total_fraud_transactions,
    ROUND(AVG(amount), 2) AS average_fraud_amount,
    ROUND(MIN(amount), 2) AS minimum_fraud_amount,
    ROUND(MAX(amount), 2) AS maximum_fraud_amount,
    ROUND(SUM(amount), 2) AS total_fraud_amount
FROM fraud_transactions
WHERE isFraud = 1;


-- Query 07: Analyze sender balances in fraud-labelled transactions

SELECT
    COUNT(*) AS total_fraud_transactions,

    SUM(CASE
        WHEN oldbalanceOrg > 0 THEN 1
        ELSE 0
    END) AS sender_had_balance,

    SUM(CASE
        WHEN newbalanceOrig = 0 THEN 1
        ELSE 0
    END) AS sender_balance_became_zero,

    ROUND(AVG(amount), 2) AS average_transaction_amount

FROM fraud_transactions
WHERE isFraud = 1;

-- Query 08: Analyze receiver balances in fraud-labelled transactions

SELECT
    COUNT(*) AS total_fraud_transactions,

    SUM(CASE
        WHEN oldbalanceDest = 0 THEN 1
        ELSE 0
    END) AS receiver_balance_was_zero,

    SUM(CASE
        WHEN newbalanceDest > oldbalanceDest THEN 1
        ELSE 0
    END) AS receiver_balance_increased,

    ROUND(AVG(oldbalanceDest), 2) AS average_old_receiver_balance,

    ROUND(AVG(newbalanceDest), 2) AS average_new_receiver_balance

FROM fraud_transactions
WHERE isFraud = 1;

-- Query 09: Evaluate system flags against fraud labels

SELECT
    isFraud,
    isFlaggedFraud,
    COUNT(*) AS total_transactions
FROM fraud_transactions
GROUP BY isFraud, isFlaggedFraud
ORDER BY isFraud, isFlaggedFraud;

-- Query 10: Calculate fraud miss rate

SELECT
    COUNT(*) AS total_fraud_transactions,

    SUM(CASE
        WHEN isFlaggedFraud = 0 THEN 1
        ELSE 0
    END) AS fraud_transactions_not_flagged,

    ROUND(
        SUM(CASE
            WHEN isFlaggedFraud = 0 THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        4
    ) AS fraud_miss_rate_percentage

FROM fraud_transactions
WHERE isFraud = 1;

-- Query 11: Count normal-labelled transactions flagged by the system

SELECT
    COUNT(*) AS total_normal_transactions,

    SUM(CASE
        WHEN isFlaggedFraud = 1 THEN 1
        ELSE 0
    END) AS normal_transactions_flagged,

    ROUND(
        SUM(CASE
            WHEN isFlaggedFraud = 1 THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        4
    ) AS false_positive_rate_percentage

FROM fraud_transactions
WHERE isFraud = 0;



-- Query 12: Analyze high-value transactions


SELECT
    'High Value' AS transaction_category,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(SUM(isFraud) * 100.0 / COUNT(*), 4)
        AS fraud_percentage,
    ROUND(AVG(amount), 2) AS average_amount
FROM fraud_transactions
WHERE amount >= 1000000;


-- Query 13: Analyze transactions below the high-value threshold

SELECT
    'Other Transactions' AS transaction_category,
    COUNT(*) AS total_transactions,
    SUM(isFraud) AS fraud_transactions,
    ROUND(
        SUM(isFraud) * 100.0 / COUNT(*),
        4
    ) AS fraud_percentage,
    ROUND(AVG(amount), 2) AS average_amount
FROM fraud_transactions
WHERE amount < 1000000;















