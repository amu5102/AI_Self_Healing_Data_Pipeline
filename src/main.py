import pandas as pd

from src.transformation.transform import transform_data
from src.load import load_to_database

from src.failure_logging.logger import log_failure

from src.validation.validate import (
    EXPECTED_COLUMNS,
    validate_data
)

from src.failure_detection.detector import (
    detect_schema_failure,
    detect_null_failure,
    detect_duplicate_failure,
    detect_data_type_failure,
    print_failure_report
)

from src.root_cause.analyzer import (
    analyze_schema_failure,
    analyze_null_failure,
    analyze_duplicate_failure,
    analyze_data_type_failure,
    print_root_cause_report
)

from src.self_healing.healer import (
    apply_schema_healing,
    verify_healing,
    apply_null_healing,
    verify_null_healing,
    apply_duplicate_healing,
    verify_duplicate_healing,
    apply_data_type_healing,
    verify_data_type_healing
)

from src.ml.predictor import predict_failure


def run_pipeline(file_path):
    """
    Run the complete AI self-healing data pipeline.
    """

    print("\n")
    print("==============================================")
    print("   AI SELF-HEALING DATA PIPELINE")
    print("==============================================")

    # STEP 1: EXTRACT DATA
    print("\n[1] DATA EXTRACTION")

    df = pd.read_csv(file_path)

    print("Data extracted successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # STEP 2: VALIDATE DATA
    print("\n[2] DATA VALIDATION")

    validation_result = validate_data(df)

    # Variables used for failure logging
    failure = None
    root_cause = None
    healing_action = "No automatic healing"
    failure_status = "SUCCESS"

    # STEP 3: FAILURE DETECTION
    print("\n[3] FAILURE DETECTION")

    schema_failure = detect_schema_failure(
        EXPECTED_COLUMNS,
        list(df.columns)
    )

    null_failure = detect_null_failure(df)
    
    duplicate_failure = detect_duplicate_failure(df)
    
    data_type_failure = detect_data_type_failure(df)
    
    if schema_failure is not None:

        failure = schema_failure

        print_failure_report(failure)

        # STEP 4: ROOT CAUSE ANALYSIS
        print("\n[4] ROOT CAUSE ANALYSIS")

        root_cause = analyze_schema_failure(
            failure
        )

        print_root_cause_report(root_cause)
        
        ml_prediction = predict_failure(
            severity=failure["severity"],
            root_cause_type=root_cause["root_cause_type"],
            confidence=root_cause["confidence"],
            duplicate_count=0,
            null_count=0,
            schema_change=1
        )

        print("\n========== ML FAILURE PREDICTION ==========")
        print(f"Predicted Failure Type : {ml_prediction}")
        print("==========================================")

        # STEP 5: SELF-HEALING
        print("\n[5] SELF-HEALING")

        df, healed = apply_schema_healing(
            df,
            root_cause
        )

        if not healed:
            print("\nSelf-healing was not successful.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        # STEP 6: HEALING VERIFICATION
        print("\n[6] HEALING VERIFICATION")

        verification_result = verify_healing(
            df,
            EXPECTED_COLUMNS
        )

        if not verification_result:
            print("\nHealing verification failed.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        # Create healing action description
        if root_cause.get("possible_mappings"):

            mapping = root_cause[
                "possible_mappings"
            ][0]

            healing_action = (
                f"{mapping['actual_column']} "
                f"-> "
                f"{mapping['expected_column']}"
            )

        failure_status = "HEALED"

    elif null_failure is not None:

        failure = null_failure

        print_failure_report(failure)

        # STEP 4: ROOT CAUSE ANALYSIS
        print("\n[4] ROOT CAUSE ANALYSIS")

        root_cause = analyze_null_failure(
            failure
        )

        print_root_cause_report(root_cause)
        
        ml_prediction = predict_failure(
            severity=failure["severity"],
            root_cause_type=root_cause["root_cause_type"],
            confidence=root_cause["confidence"],
            duplicate_count=0,
            null_count=sum(failure["null_columns"].values()),
            schema_change=0
        )

        print("\n========== ML FAILURE PREDICTION ==========")
        print(f"Predicted Failure Type : {ml_prediction}")
        print("==========================================")
        
        # STEP 5: SELF-HEALING
        print("\n[5] SELF-HEALING")

        df, healed = apply_null_healing(
            df,
            root_cause
        )

        if not healed:
            print("\nSelf-healing was not successful.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        # STEP 6: HEALING VERIFICATION
        print("\n[6] HEALING VERIFICATION")

        verification_result = verify_null_healing(
            df
        )

        if not verification_result:
            print("\nHealing verification failed.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        affected_columns = root_cause.get(
            "affected_columns",
            []
        )

        healing_action = (
            "NULL values repaired in: "
            + ", ".join(affected_columns)
        )

        failure_status = "HEALED"
    
    elif duplicate_failure is not None:
    
        failure = duplicate_failure

        print_failure_report(failure)

        # STEP 4: ROOT CAUSE ANALYSIS
        print("\n[4] ROOT CAUSE ANALYSIS")

        root_cause = analyze_duplicate_failure(
            failure
        )

        print_root_cause_report(root_cause)
        
        ml_prediction = predict_failure(
            severity=failure["severity"],
            root_cause_type=root_cause["root_cause_type"],
            confidence=root_cause["confidence"],
            duplicate_count=failure["duplicate_count"],
            null_count=0,
            schema_change=0
        )

        print("\n========== ML FAILURE PREDICTION ==========")
        print(f"Predicted Failure Type : {ml_prediction}")
        print("==========================================")

        # STEP 5: SELF-HEALING
        print("\n[5] SELF-HEALING")

        df, healed = apply_duplicate_healing(
            df,
            root_cause
        )

        if not healed:
            print("\nSelf-healing was not successful.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        # STEP 6: HEALING VERIFICATION
        print("\n[6] HEALING VERIFICATION")

        verification_result = verify_duplicate_healing(
            df
        )

        if not verification_result:
            print("\nHealing verification failed.")
            print("Pipeline stopped.")

            log_failure(
                failure,
                root_cause,
                healing_action,
                "FAILED"
            )

            return None

        duplicate_count = root_cause.get(
            "duplicate_count",
            0
        )

        healing_action = (
            f"Removed {duplicate_count} "
            f"duplicate record(s)"
        )

        failure_status = "HEALED"
    
    elif data_type_failure is not None:
    
        failure = data_type_failure

        print_failure_report(failure)

        # STEP 4: ROOT CAUSE ANALYSIS
        print("\n[4] ROOT CAUSE ANALYSIS")

        root_cause = analyze_data_type_failure(
            failure,
            df
        )

        print_root_cause_report(root_cause)

        # STEP 5: SELF-HEALING
        print("\n[5] SELF-HEALING")

        df, healed = apply_data_type_healing(
            df,
            root_cause
        )

        if not healed:
    
            print("\nAutomatic data type healing was not possible.")
            print("Manual review is required.")
            print("Pipeline stopped.")

            healing_action = (
                "Manual review required for invalid data type"
            )

            failure_status = "FAILED"

            log_failure(
                failure,
                root_cause,
                healing_action,
                failure_status
            )

            return None

        else:

            healing_action = (
                "Safely converted invalid data type values"
            )

            failure_status = "HEALED"

        # STEP 6: HEALING VERIFICATION
        print("\n[6] HEALING VERIFICATION")

        if healed:

            verification_result = verify_data_type_healing(
                df,
                root_cause.get(
                    "affected_columns",
                    []
                )
            )

            if not verification_result:

                print("Pipeline stopped.")

                log_failure(
                    failure,
                    root_cause,
                    healing_action,
                    "FAILED"
                )

                return None

        else:

            print(
                "Verification skipped because "
                "healing was not successful."
            )
    
    else:

        print("No failure detected.")

        print("\n[4] ROOT CAUSE ANALYSIS")
        print("No root cause analysis required.")

        print("\n[5] SELF-HEALING")
        print("No healing action required.")

        print("\n[6] HEALING VERIFICATION")
        print("No healing required.")

    # FAILURE LOGGING
    if failure is not None:

        log_failure(
            failure,
            root_cause,
            healing_action,
            failure_status
        )

    # STEP 7: DATA TRANSFORMATION
    print("\n[7] DATA TRANSFORMATION")

    df = transform_data(df)

    # STEP 8: SQL DATABASE LOADING
    print("\n[8] SQL DATABASE LOADING")

    database_result = load_to_database(df)

    if not database_result:
        print("\nDatabase loading failed.")
        print("Pipeline stopped.")
        return None

    # STEP 9: FINAL PIPELINE RESULT
    print("\n==============================================")
    print("FINAL PIPELINE STATUS: SUCCESS")
    print("==============================================")

    print("\nFinal Columns:")
    print(list(df.columns))

    print(f"\nFinal rows processed: {len(df)}")

    return df


if __name__ == "__main__":

    # Test with schema-changed data

    file_path = "data/raw/customers.csv"

    result = run_pipeline(file_path)

    if result is not None:

        print("\nPipeline completed successfully.")

    else:

        print("\nPipeline execution failed.")