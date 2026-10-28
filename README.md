# Financial ETL — Transaction Processing with Python and SQL Server

An ETL (Extract, Transform, Load) pipeline developed as a data engineering learning project. It processes **10,000 financial transactions** from a CSV file, applies validation and risk classification rules, separates records for review, and stores legitimate transactions in SQL Server.

> **Scope:** Educational project. Risk thresholds are illustrative rules and do not constitute a validated banking fraud detection system.

## Architecture

```text
Transaction CSV
       |
       v
 extract.py   --> read data with pandas
       |
       v
 transform.py --> classify and route records
       |
       +--> legitimate transactions with positive amounts --> load.py --> SQL Server
       +--> records flagged as fraud ---------------------> data/output/fraudes.csv
       +--> records with amount <= 0 ---------------------> data/output/cuarentena.csv
```

`main.py` orchestrates the entire pipeline.

## Technologies

- **Python 3.14** and **pandas:** data extraction, exploration, and transformation.
- **SQL Server 2025 Express:** storage of legitimate transactions.
- **SQLAlchemy**, **pyodbc**, and **ODBC Driver 18 for SQL Server:** database connectivity and data loading.
- **pytest:** automated testing.
- **VS Code / Jupyter:** development and dataset exploration.

## Business Rules

### Risk classification

The `nivel_riesgo` column is created based on `device_trust_score` and `velocity_last_24h`:

| Level | Rule |
| --- | --- |
| ALTO (High) | `device_trust_score < 40` **and** `velocity_last_24h > 5` |
| MEDIO (Medium) | **Exactly one** of the two conditions is met |
| BAJO (Low) | Neither condition is met |

The Spanish category values are preserved because they are the actual values produced by the code.

### Transaction routing

Rules are applied in the following order so that each record has exactly one destination:

1. **Quarantine:** `amount <= 0`, regardless of the fraud flag.
2. **Fraud audit:** `amount > 0` and `is_fraud == 1`.
3. **Main table:** `amount > 0` and `is_fraud == 0`.

Records routed for review are not deleted. The system assumes that `amount` and `is_fraud` contain valid values; more comprehensive type, null, and range validation is required before processing different external datasets.

## Test Dataset Results

| Destination | Records |
| --- | ---: |
| SQL Server (`dbo.Transacciones`) | 9,848 |
| Fraud audit (`fraudes.csv`) | 151 |
| Quarantine (`cuarentena.csv`) | 1 |
| **Total** | **10,000** |

One transaction with a zero amount (`transaction_id = 2903`) was identified and routed for review. A second execution was verified to avoid reinserting previously loaded IDs.

## Project Structure

```text
ETL_proyect/
├── data/
│   ├── credit_card_fraud_10k.csv  # Local file; not committed to Git
│   └── output/                    # Generated files; ignored by Git
├── notebooks/
│   └── exploracion.ipynb
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── tests/
│   └── test_transform.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python and `pip`.
- SQL Server Express installed and running.
- An existing `ETL_Financiero` database and `dbo.Transacciones` table.
- ODBC Driver 18 for SQL Server.
- Access to the `localhost\SQLEXPRESS` instance through Windows integrated authentication.

> **Important:** The current version uses a local connection configuration in `src/load.py`. The server instance, database, and certificate settings may need to be adjusted on other machines. `TrustServerCertificate=yes` is used only for the local learning environment.

### Reference SQL schema

Run this script in SSMS against `ETL_Financiero` before the first load:

```sql
USE ETL_Financiero;
GO

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
GO
```

Do not rerun `CREATE TABLE` if the table already exists.

## Installation and Usage (Windows PowerShell)

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Place the input CSV at `data/credit_card_fraud_10k.csv` and review the connection settings in `src/load.py`.

Run the pipeline:

```powershell
python src/main.py
```

Run the tests:

```powershell
python -m pytest -v
```

## Tests

**Four automated tests** have been implemented to verify:

- ALTO, MEDIO, and BAJO risk classifications.
- Routing of sample transactions into the three output groups, including checks that IDs do not overlap between groups.

Last observed run: **4 tests passed**.

## Limitations and Planned Improvements

- Duplicate prevention checks existing IDs before inserting: this works for sequential executions in the example but is **not safe for concurrent loads**.
- Existing records are not updated if their contents change in a later run.
- SQL Server integration tests, comprehensive input validation, logging, and more detailed error handling have not yet been implemented.
- Risk rules and thresholds have not been calibrated or validated against real-world financial requirements.
- Check the dataset's license before publishing it, and avoid including personal or sensitive information.

## Visual Evidence (Optional)

You can add a `docs/images/` directory with screenshots **that contain no sensitive data** and reference them here:

```markdown
![ETL execution](docs/images/ejecucion-etl.png)
![Records loaded into SQL Server](docs/images/sql-server-resultados.png)
![Automated tests](docs/images/pruebas-pytest.png)
```

Screenshots document results, but **do not replace reproducible instructions or tests**.

## Purpose

This project was built to practice an end-to-end data engineering workflow: extraction, data profiling, validation, transformation, relational database loading, testing, and modular code organization.
