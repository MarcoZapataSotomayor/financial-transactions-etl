
from pathlib import Path
from extract import extract_data
from transform import transform_data
from load import load_data
from load import export_audit_files

def main():
    # Obtener la carpeta principal del proyecto
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Construir la ruta del CSV
    csv_path = BASE_DIR / "data" / "credit_card_fraud_10k.csv"

    # Ejecutar la extracción
    df = extract_data(csv_path)

    df_valid, df_quarantine, df_fraud = transform_data(df)
    export_audit_files(df_fraud, df_quarantine)

    load_data(df_valid)
    print("Carga de transacciones completada.")

    print(f"Transacciones válidas: {len(df_valid)}")
    print(f"Transacciones en cuarentena: {len(df_quarantine)}")
    print(f"Transacciones fraudulentas: {len(df_fraud)}")

    print(f"Total procesado: {len(df_valid) + len(df_quarantine) + len(df_fraud)}")
    

    # Mostrar un resumen
    print("Extracción completada.")
    print(f"Registros extraídos: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    main()
