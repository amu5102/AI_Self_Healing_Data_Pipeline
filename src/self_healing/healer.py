def rename_column(df, old_name, new_name):
    """
    Rename a column in the DataFrame.
    """

    if old_name not in df.columns:
        print(f"Healing FAILED: column '{old_name}' not found")
        return df, False

    if new_name in df.columns:
        print(
            f"Healing FAILED: column '{new_name}' "
            f"already exists"
        )
        return df, False

    df = df.rename(
        columns={
            old_name: new_name
        }
    )

    print(
        f"Healing action applied: "
        f"{old_name} → {new_name}"
    )

    return df, True


def apply_schema_healing(df, root_cause):
    """
    Apply automatic healing based on root cause analysis.
    """

    if root_cause is None:
        print("No healing action required")
        return df, False

    root_cause_type = root_cause["root_cause_type"]

    if root_cause_type != "POSSIBLE_COLUMN_RENAME":
        print("No automatic healing rule available")
        return df, False

    mappings = root_cause["possible_mappings"]

    if not mappings:
        print("No column mapping available")
        return df, False

    healed = False

    for mapping in mappings:

        old_name = mapping["actual_column"]
        new_name = mapping["expected_column"]

        similarity = mapping["similarity"]

        # Safety threshold
        if similarity >= 0.5:

            df, success = rename_column(
                df,
                old_name,
                new_name
            )

            if success:
                healed = True

    return df, healed

def verify_healing(df, expected_columns):
    """
    Verify that the healed DataFrame matches
    the expected schema.
    """

    actual_columns = list(df.columns)

    missing_columns = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    extra_columns = [
        column
        for column in actual_columns
        if column not in expected_columns
    ]

    if not missing_columns and not extra_columns:

        print("\nHealing verification PASSED")
        print("Dataset now matches the expected schema")

        return True

    print("\nHealing verification FAILED")

    if missing_columns:
        print(
            f"Still missing: {missing_columns}"
        )

    if extra_columns:
        print(
            f"Still extra: {extra_columns}"
        )

    return False

def apply_null_healing(df, root_cause):
    """
    Automatically repair NULL values using
    column-specific healing rules.
    """

    if root_cause is None:
        print("No NULL healing required")
        return df, False

    if root_cause.get("root_cause_type") != "MISSING_DATA":
        print("No NULL healing rule available")
        return df, False

    healed = False

    affected_columns = root_cause.get(
        "affected_columns",
        []
    )

    # Heal missing email values
    if "email" in affected_columns:

        null_count = df["email"].isnull().sum()

        df["email"] = df["email"].fillna(
            "unknown@email.com"
        )

        print(
            f"NULL healing applied to email: "
            f"{null_count} value(s) replaced"
        )

        healed = True

    # Heal missing age values
    if "age" in affected_columns:

        null_count = df["age"].isnull().sum()

        median_age = df["age"].median()

        df["age"] = df["age"].fillna(
            median_age
        )

        print(
            f"NULL healing applied to age: "
            f"{null_count} value(s) replaced "
            f"with median age {median_age}"
        )

        healed = True

    return df, healed

def verify_null_healing(df):
    """
    Verify that no NULL values remain after healing.
    """

    null_counts = df.isnull().sum()

    remaining_nulls = {
        column: int(count)
        for column, count in null_counts.items()
        if count > 0
    }

    if not remaining_nulls:
        print("\nNULL healing verification PASSED")
        print("No NULL values remain in the dataset")
        return True

    print("\nNULL healing verification FAILED")
    print(
        f"Remaining NULL values: {remaining_nulls}"
    )

    return False

def apply_duplicate_healing(df, root_cause):
    """
    Automatically remove duplicate records.
    """

    if root_cause is None:
        print("No duplicate healing required")
        return df, False

    if root_cause.get("root_cause_type") != "DUPLICATE_RECORDS":
        print("No duplicate healing rule available")
        return df, False

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count == 0:
        print("No duplicate records found")
        return df, False

    df = df.drop_duplicates().copy()

    print(
        f"Duplicate healing applied: "
        f"{duplicate_count} duplicate record(s) removed"
    )

    return df, True

def verify_duplicate_healing(df):
    """
    Verify that no duplicate records remain.
    """

    remaining_duplicates = int(
        df.duplicated().sum()
    )

    if remaining_duplicates == 0:

        print("\nDuplicate healing verification PASSED")
        print("No duplicate records remain in the dataset")

        return True

    print("\nDuplicate healing verification FAILED")
    print(
        f"Remaining duplicate records: "
        f"{remaining_duplicates}"
    )

    return False