import pandas as pd


def transform_data(df):
    """
    Clean and transform the validated customer data.
    """

    print("\n========== DATA TRANSFORMATION ==========")

    # Make a copy so the original DataFrame is not modified
    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate records
    before_duplicates = len(df)

    df = df.drop_duplicates()

    after_duplicates = len(df)

    removed_duplicates = (
        before_duplicates - after_duplicates
    )

    # Standardize text columns
    df["customer_name"] = (
        df["customer_name"]
        .astype(str)
        .str.strip()
    )

    df["email"] = (
        df["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["city"] = (
        df["city"]
        .astype(str)
        .str.strip()
    )

    # Convert age to numeric
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    print("Transformation completed successfully")
    print(f"Rows before transformation : {before_duplicates}")
    print(f"Duplicates removed         : {removed_duplicates}")
    print(f"Rows after transformation  : {len(df)}")

    print("\nTransformed columns:")
    print(list(df.columns))

    print("==========================================")

    return df


if __name__ == "__main__":

    file_path = "data/raw/customers.csv"

    df = pd.read_csv(file_path)

    transformed_df = transform_data(df)

    print("\nTransformed Data:")
    print(transformed_df)