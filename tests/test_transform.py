from src.transform import risk_classification
import pandas as pd
from src.transform import transform_data


def test_riesgo_alto():
    resultado = risk_classification(25, 9)
    assert resultado == "ALTO"


def test_riesgo_medio():
    resultado = risk_classification(35, 1)
    assert resultado == "MEDIO"


def test_riesgo_bajo():
    resultado = risk_classification(90, 2)
    assert resultado == "BAJO"

def test_distribucion_transacciones():
    datos = pd.DataFrame({
        "transaction_id": [1, 2, 3, 4],
        "amount": [100.0, 0.0, 250.0, 50.0],
        "is_fraud": [0, 0, 1, 0],
        "device_trust_score": [80, 35, 25, 90],
        "velocity_last_24h": [1, 2, 9, 1]
    })

    valid, quarantine, fraud = transform_data(datos)

    assert len(valid) == 2
    assert len(quarantine) == 1
    assert len(fraud) == 1

    assert len(valid) + len(quarantine) + len(fraud) == len(datos)
    ids_valid = set(valid["transaction_id"])
    ids_quarantine = set(quarantine["transaction_id"])
    ids_fraud = set(fraud["transaction_id"])

    assert ids_valid.isdisjoint(ids_quarantine)
    assert ids_valid.isdisjoint(ids_fraud)
    assert ids_quarantine.isdisjoint(ids_fraud)

    