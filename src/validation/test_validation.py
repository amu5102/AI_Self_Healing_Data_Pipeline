import pandas as pd

from validate import validate_data


df = pd.read_csv("data/raw/customers.csv")

validate_data(df)