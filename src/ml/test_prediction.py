import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


DATA_FILE = "data/processed/ml_failure_history.csv"


# Load dataset
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


# Encode categorical columns
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


# Encode target
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)


# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y_encoded)


# New failure example
new_failure = pd.DataFrame([{
    "severity": "MEDIUM",
    "root_cause_type": "MISSING_DATA",
    "confidence": "HIGH",
    "duplicate_count": 0,
    "null_count": 5,
    "schema_change": 0
}])


# Encode new failure
for column in categorical_columns:
    new_failure[column] = label_encoders[column].transform(
        new_failure[column]
    )


# Prediction
prediction = model.predict(new_failure)

predicted_failure_type = target_encoder.inverse_transform(
    prediction
)[0]


print("\n==========================================")
print("ML FAILURE PREDICTION TEST")
print("==========================================")

print("New Failure:")
print("Severity          : MEDIUM")
print("Root Cause        : MISSING_DATA")
print("Confidence        : HIGH")
print("NULL Count        : 5")
print("Schema Change     : 0")

print("\nPredicted Failure Type:")
print(predicted_failure_type)

print("==========================================")