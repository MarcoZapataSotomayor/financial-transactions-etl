
IF DB_ID('ETL_Financiero') IS NULL
BEGIN
    CREATE DATABASE ETL_Financiero;
END;
GO

USE ETL_Financiero;
GO

IF OBJECT_ID('dbo.Transacciones', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Transacciones (
        transaction_id INT PRIMARY KEY,
        amount DECIMAL(12,2) NOT NULL,
        transaction_hour TINYINT,
        merchant_category VARCHAR(50),
        foreign_transaction BIT,
        location_mismatch BIT,
        device_trust_score TINYINT,
        velocity_last_24h INT,
        cardholder_age TINYINT,
        is_fraud BIT,
        nivel_riesgo VARCHAR(5)
    );
END;
GO
