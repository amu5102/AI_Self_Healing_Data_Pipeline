import pandas as pd


EXPECTED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "city",
    "age"
]


def validate_schema(df):
    """Validate whether the dataset has the expected columns."""

    actual_columns = list(df.columns)

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    extra_columns = [
        column for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        print("Schema validation FAILED")
        print(f"Missing columns: {missing_columns}")
        return False

    if extra_columns:
        print("Schema validation FAILED")
        print(f"Extra columns: {extra_columns}")
        return False

    print("Schema validation PASSED")
    return True


def validate_nulls(df):
    """Check for missing values."""

    null_counts = df.isnull().sum()

    total_nulls = null_counts.sum()

    if total_nulls > 0:
        print("Null validation FAILED")
        print(null_counts[null_counts > 0])
        return False

    print("Null validation PASSED")
    return True


def validate_duplicates(df):
    """Check for duplicate records."""

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        print("Duplicate validation FAILED")
        print(f"Duplicate records: {duplicate_count}")
        return False

    print("Duplicate validation PASSED")
    return True


def validate_data_types(df):
    """Check important column data types."""

    required_columns = ["customer_id", "age"]

    for column in required_columns:
        if column not in df.columns:
            print("Data type validation SKIPPED")
            print(f"Column '{column}' is missing")
            return False

    if not pd.api.types.is_numeric_dtype(df["customer_id"]):
        print("Data type validation FAILED")
        print("customer_id must be numeric")
        return False

    if not pd.api.types.is_numeric_dtype(df["age"]):
        print("Data type validation FAILED")
        print("age must be numeric")
        return False

    print("Data type validation PASSED")
    return True


def validate_data(df):
    """Run all data-quality validations."""

    print("\n========== DATA VALIDATION ==========\n")

    schema_valid = validate_schema(df)
    nulls_valid = validate_nulls(df)
    duplicates_valid = validate_duplicates(df)
    types_valid = validate_data_types(df)

    validation_result = (
        schema_valid
        and nulls_valid
        and duplicates_valid
        and types_valid
    )

    print("\n=====================================")

    if validation_result:
        print("OVERALL VALIDATION: PASSED")
    else:
        print("OVERALL VALIDATION: FAILED")

    print("=====================================\n")

    return validation_result