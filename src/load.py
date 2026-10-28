import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from pathlib import Path
from sqlalchemy import text

def test_connection():
    """test local conection with SQL Server"""

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=ETL_Financiero;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    with pyodbc.connect(connection_string, timeout=5) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DB_NAME(), @@SERVERNAME")
        result = cursor.fetchone()

        print(f"Base de datos: {result[0]}")
        print(f"Servidor: {result[1]}")


def load_data(df):
    """Carga las transacciones válidas en SQL Server."""

    connection_url = URL.create(
        "mssql+pyodbc",
        host=r"localhost\SQLEXPRESS",
        database="ETL_Financiero",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Trusted_Connection": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_engine(connection_url)

    
    try:
        existing_ids = get_existing_ids(engine)

        df_new = df[
            ~df["transaction_id"].isin(existing_ids)
        ].copy()

        if df_new.empty:
            print("No hay transacciones nuevas para insertar.")
            return

        with engine.begin() as connection:
            df_new.to_sql(
                name="Transacciones",
                con=connection,
                schema="dbo",
                if_exists="append",
                index=False,
                chunksize=500
            )

        print(f"Se insertaron {len(df_new)} transacciones nuevas.")

    finally:
        engine.dispose()


def export_audit_files(df_fraud, df_quarantine):
    """Exporta los registros de fraude y cuarentena."""

    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "data" / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    df_fraud.to_csv(output_dir / "fraudes.csv", index=False)
    df_quarantine.to_csv(output_dir / "cuarentena.csv", index=False)

    print("Archivos de auditoría exportados correctamente.")

def get_existing_ids(engine):
    """Obtiene los IDs de transacciones existentes en SQL Server."""

    query = text("SELECT transaction_id FROM dbo.Transacciones")

    with engine.connect() as connection:
        df_existing = pd.read_sql(query, connection)

    return set(df_existing["transaction_id"])

if __name__ == "__main__":
    test_connection()


