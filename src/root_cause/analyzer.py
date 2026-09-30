from difflib import SequenceMatcher


def calculate_similarity(text1, text2):
    """Calculate similarity between two column names."""

    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()


def analyze_schema_failure(failure):
    """
    Analyze a schema failure and identify
    possible root causes.
    """

    if failure is None:
        return None

    missing_columns = failure["missing_columns"]
    extra_columns = failure["extra_columns"]

    possible_mappings = []

    for missing in missing_columns:
        for extra in extra_columns:

            similarity = calculate_similarity(
                missing,
                extra
            )

            if similarity >= 0.5:
                possible_mappings.append({
                    "expected_column": missing,
                    "actual_column": extra,
                    "similarity": round(similarity, 2)
                })

    if possible_mappings:

        root_cause = {
            "root_cause_type": "POSSIBLE_COLUMN_RENAME",
            "description": (
                "A required column appears to have been "
                "renamed in the source dataset."
            ),
            "possible_mappings": possible_mappings,
            "confidence": "MEDIUM"
        }

    else:

        root_cause = {
            "root_cause_type": "UNKNOWN_SCHEMA_CHANGE",
            "description": (
                "The dataset schema does not match "
                "the expected schema."
            ),
            "possible_mappings": [],
            "confidence": "LOW"
        }

    return root_cause

def print_root_cause_report(root_cause):
    """Display the root cause analysis."""

    if root_cause is None:
        print("No root cause analysis required.")
        return

    print("\n========== ROOT CAUSE ANALYSIS ==========")

    print(
        f"Root Cause Type : "
        f"{root_cause['root_cause_type']}"
    )

    print(
        f"Description     : "
        f"{root_cause['description']}"
    )

    print(
        f"Confidence      : "
        f"{root_cause['confidence']}"
    )

    # Schema-change RCA
    if root_cause["root_cause_type"] == "POSSIBLE_COLUMN_RENAME":

        if root_cause.get("possible_mappings"):

            print("\nPossible Column Mapping:")

            for mapping in root_cause["possible_mappings"]:

                print(
                    f"  {mapping['actual_column']} "
                    f"→ "
                    f"{mapping['expected_column']} "
                    f"(similarity: "
                    f"{mapping['similarity']})"
                )

    # NULL-data RCA
    elif root_cause["root_cause_type"] == "MISSING_DATA":

        print(
            f"\nAffected Columns: "
            f"{root_cause['affected_columns']}"
        )

        print(
            f"NULL Counts     : "
            f"{root_cause['null_counts']}"
        )

        print(
            f"Total NULLs     : "
            f"{root_cause['total_nulls']}"
        )

    print("==========================================\n")

def analyze_null_failure(failure):
    """
    Analyze a NULL-data failure and identify
    the affected columns.
    """

    if failure is None:
        return None

    null_columns = failure.get(
        "null_columns",
        {}
    )

    if not null_columns:
        return {
            "root_cause_type": "NO_NULL_DATA",
            "description": "No NULL values were detected.",
            "confidence": "HIGH"
        }

    affected_columns = list(
        null_columns.keys()
    )

    total_nulls = sum(
        null_columns.values()
    )

    root_cause = {
        "root_cause_type": "MISSING_DATA",
        "description": (
            "Required data is missing from "
            "one or more columns."
        ),
        "affected_columns": affected_columns,
        "null_counts": null_columns,
        "total_nulls": total_nulls,
        "confidence": "HIGH"
    }

    return root_cause

def analyze_duplicate_failure(failure):
    """
    Analyze a duplicate-data failure and identify
    the number of duplicate records.
    """

    if failure is None:
        return None

    duplicate_count = failure.get(
        "duplicate_count",
        0
    )

    if duplicate_count == 0:
        return {
            "root_cause_type": "NO_DUPLICATES",
            "description": "No duplicate records were detected.",
            "confidence": "HIGH"
        }

    root_cause = {
        "root_cause_type": "DUPLICATE_RECORDS",
        "description": (
            "One or more duplicate records were "
            "detected in the input dataset."
        ),
        "duplicate_count": duplicate_count,
        "confidence": "HIGH"
    }

    return root_cause