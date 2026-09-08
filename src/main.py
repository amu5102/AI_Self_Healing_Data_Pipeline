import pandas as pd

from src.validation.validate import (
    EXPECTED_COLUMNS,
    validate_data
)

from src.failure_detection.detector import (
    detect_schema_failure,
    print_failure_report
)

from src.root_cause.analyzer import (
    analyze_schema_failure,
    print_root_cause_report
)

from src.self_healing.healer import (
    apply_schema_healing,
    verify_healing
)


def run_pipeline(file_path):
    """
    Run the complete self-healing data pipeline.
    """

    print("\n")
    print("==============================================")
    print("   AI SELF-HEALING DATA PIPELINE")
    print("==============================================")

    # ------------------------------------------
    # STEP 1: EXTRACT DATA
    # ------------------------------------------

    print("\n[1] DATA EXTRACTION")

    df = pd.read_csv(file_path)

    print("Data extracted successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # ------------------------------------------
    # STEP 2: VALIDATE DATA
    # ------------------------------------------

    print("\n[2] DATA VALIDATION")

    validation_result = validate_data(df)

    # ------------------------------------------
    # STEP 3: CHECK VALIDATION RESULT
    # ------------------------------------------

    if validation_result:

        print("\nData validation successful.")
        print("No healing required.")

        return df

    # ------------------------------------------
    # STEP 4: FAILURE DETECTION
    # ------------------------------------------

    print("\n[3] FAILURE DETECTION")

    actual_columns = list(df.columns)

    failure = detect_schema_failure(
        EXPECTED_COLUMNS,
        actual_columns
    )

    print_failure_report(failure)

    # ------------------------------------------
    # STEP 5: ROOT CAUSE ANALYSIS
    # ------------------------------------------

    print("\n[4] ROOT CAUSE ANALYSIS")

    root_cause = analyze_schema_failure(
        failure
    )

    print_root_cause_report(root_cause)

    # ------------------------------------------
    # STEP 6: SELF-HEALING
    # ------------------------------------------

    print("\n[5] SELF-HEALING")

    df, healed = apply_schema_healing(
        df,
        root_cause
    )

    if not healed:

        print("\nSelf-healing was not successful.")
        print("Pipeline stopped.")

        return None

    # ------------------------------------------
    # STEP 7: VERIFY HEALING
    # ------------------------------------------

    print("\n[6] HEALING VERIFICATION")

    verification_result = verify_healing(
        df,
        EXPECTED_COLUMNS
    )

    # ------------------------------------------
    # STEP 8: FINAL RESULT
    # ------------------------------------------

    print("\n==============================================")

    if verification_result:

        print("FINAL PIPELINE STATUS: SUCCESS")

        print("==============================================")

        print("\nFinal Columns:")
        print(list(df.columns))

        return df

    else:

        print("FINAL PIPELINE STATUS: FAILED")

        print("==============================================")

        return None


if __name__ == "__main__":

    # Test with schema-changed data
    file_path = "data/raw/customers_schema_changed.csv"

    result = run_pipeline(file_path)

    if result is not None:

        print("\nPipeline completed successfully.")
        print(f"Final rows processed: {len(result)}")

    else:

        print("\nPipeline execution failed.")