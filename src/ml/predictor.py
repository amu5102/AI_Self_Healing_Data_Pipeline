import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


DATA_FILE = "data/processed/ml_failure_history.csv"


def train_model():

    df = pd.read_csv(DATA_FILE)

    feature_columns = [
        "severity",
        "root_cause_type",
        "confidence",
        "duplicate_count",
        "null_count",
        "schema_change"
    ]

    X = df[feature_columns].copy()
    y = df["failure_type"]

    categorical_columns = [
        "severity",
        "root_cause_type",
        "confidence"
    ]

    label_encoders = {}

    for column in categorical_columns:

        encoder = LabelEncoder()

        X[column] = encoder.fit_transform(X[column])

        label_encoders[column] = encoder

    target_encoder = LabelEncoder()

    y_encoded = target_encoder.fit_transform(y)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y_encoded)

    return model, label_encoders, target_encoder


def predict_failure(
    severity,
    root_cause_type,
    confidence,
    duplicate_count,
    null_count,
    schema_change
):

    model, label_encoders, target_encoder = train_model()

    new_failure = pd.DataFrame([{
        "severity": severity,
        "root_cause_type": root_cause_type,
        "confidence": confidence,
        "duplicate_count": duplicate_count,
        "null_count": null_count,
        "schema_change": schema_change
    }])

    categorical_columns = [
        "severity",
        "root_cause_type",
        "confidence"
    ]

    for column in categorical_columns:

        new_failure[column] = label_encoders[column].transform(
            new_failure[column]
        )

    prediction = model.predict(new_failure)

    predicted_failure_type = target_encoder.inverse_transform(
        prediction
    )[0]

    return predicted_failure_type


if __name__ == "__main__":

    result = predict_failure(
        severity="MEDIUM",
        root_cause_type="MISSING_DATA",
        confidence="HIGH",
        duplicate_count=0,
        null_count=5,
        schema_change=0
    )

    print("\n==========================================")
    print("ML PREDICTOR TEST")
    print("==========================================")
    print("Predicted Failure Type:", result)
    print("==========================================")