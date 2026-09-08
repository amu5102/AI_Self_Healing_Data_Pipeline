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

    if root_cause["possible_mappings"]:

        print("\nPossible Column Mapping:")

        for mapping in root_cause["possible_mappings"]:

            print(
                f"  {mapping['actual_column']} "
                f"→ "
                f"{mapping['expected_column']} "
                f"(similarity: "
                f"{mapping['similarity']})"
            )

    print("==========================================\n")