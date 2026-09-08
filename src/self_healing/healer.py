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