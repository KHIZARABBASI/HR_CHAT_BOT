import pandas as pd
from app.database.database import engine

employees = pd.read_csv("data/EMPLOYEES1.csv")
employees["join_date"] = pd.to_datetime(
    employees["join_date"], 
    format="%d/%m/%Y",   # from DD/MM/YYYY
    errors="coerce"      # turn invalid dates into NaT instead of crashing
).dt.strftime("%Y-%m-%d")  # convert to YYYY-MM-DD string for PostgreSQL

# leaves = pd.read_csv("data/leaves.csv")
# leaves = leaves.drop(columns=["days", "approved_by"])
policies = pd.read_csv("data/policy1.csv")
salary = pd.read_csv("data/salary.csv")
salary = salary.drop(columns=["payment_date"])


# employees.to_sql("employees", engine, if_exists="append", index=False)
# leaves.to_sql("leaves", engine, if_exists="append", index=False)
# policies.to_sql("policies", engine, if_exists="append", index=False)
salary.to_sql("salaries", engine, if_exists="append", index=False)