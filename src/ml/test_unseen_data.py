from src.ml.predictor import predict_failure


test_cases = [
    {
        "name": "Unseen Schema Failure",
        "severity": "MEDIUM",
        "root_cause_type": "POSSIBLE_COLUMN_RENAME",
        "confidence": "HIGH",
        "duplicate_count": 1,
        "null_count": 2,
        "schema_change": 1,
        "expected": "SCHEMA_CHANGE"
    },
    {
        "name": "Unseen NULL Failure",
        "severity": "HIGH",
        "root_cause_type": "MISSING_DATA",
        "confidence": "MEDIUM",
        "duplicate_count": 2,
        "null_count": 8,
        "schema_change": 0,
        "expected": "NULL_DATA"
    },
    {
        "name": "Unseen Duplicate Failure",
        "severity": "LOW",
        "root_cause_type": "DUPLICATE_RECORDS",
        "confidence": "MEDIUM",
        "duplicate_count": 5,
        "null_count": 1,
        "schema_change": 0,
        "expected": "DUPLICATE_DATA"
    }
]


print("\n==========================================")
print("       UNSEEN DATA ML TEST")
print("==========================================")

correct = 0

for case in test_cases:

    prediction = predict_failure(
        severity=case["severity"],
        root_cause_type=case["root_cause_type"],
        confidence=case["confidence"],
        duplicate_count=case["duplicate_count"],
        null_count=case["null_count"],
        schema_change=case["schema_change"]
    )

    print("\nTest Case:", case["name"])
    print("Expected :", case["expected"])
    print("Predicted:", prediction)

    if prediction == case["expected"]:
        print("Result   : PASS")
        correct += 1
    else:
        print("Result   : FAIL")


print("\n==========================================")
print(f"Unseen Test Result: {correct}/{len(test_cases)} Passed")
print("==========================================")