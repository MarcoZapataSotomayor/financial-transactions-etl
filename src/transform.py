
def risk_classification(device_trust_score, velocity_last_24h):
    if device_trust_score < 40 and velocity_last_24h > 5:
        return "ALTO"
    elif device_trust_score < 40 or velocity_last_24h > 5:
        return "MEDIO"
    else:
        return "BAJO"


def transform_data(df):
    """Clasifica el riesgo y separa las transacciones."""
    df = df.copy()

    df["nivel_riesgo"] = df.apply(
        lambda row: risk_classification(
            row["device_trust_score"],
            row["velocity_last_24h"]
        ),
        axis=1
    )

    df_valid = df[
        (df["amount"] > 0) &
        (df["is_fraud"] == 0)
    ].copy()

    df_quarantine = df[
        df["amount"] <= 0
    ].copy()

    df_fraud = df[
        (df["amount"] > 0) &
        (df["is_fraud"] == 1)
    ].copy()

    return df_valid, df_quarantine, df_fraud
