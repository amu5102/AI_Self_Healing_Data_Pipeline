import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATA_FILE = "data/processed/ml_failure_history.csv"


# Load dataset
df = pd.read_csv(DATA_FILE)

print("\n==========================================")
print("ML FAILURE PREDICTION MODEL")
print("==========================================")

print(f"Dataset rows: {len(df)}")


# Encode categorical input columns
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


# Convert categorical features into numbers
label_encoders = {}

categorical_columns = [
    "severity",
    "root_cause_type",
    "confidence"
]

for column in categorical_columns:

    encoder = LabelEncoder()

    X[column] = encoder.fit_transform(
        X[column]
    )

    label_encoders[column] = encoder


# Encode target
target_encoder = LabelEncoder()

y_encoded = target_encoder.fit_transform(y)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)


print(f"Training records: {len(X_train)}")
print(f"Testing records : {len(X_test)}")


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(
    X_train,
    y_train
)


# Predict
y_pred = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n==========================================")
print("MODEL RESULTS")
print("==========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=target_encoder.classes_
    )
)

print("==========================================")