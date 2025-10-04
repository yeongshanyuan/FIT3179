import pandas as pd


def create_daily_blood_donations():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter out rows where blood_type is 'all'.
    Filter dates to be in between 2010 to 2025.
    Save the cleaned dataset.
    """
    df = pd.read_csv("Original Datasets/Daily Blood Donations by Blood Group.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    result = df[(df["blood_type"] != "all") & (df["date"].dt.year.between(2010, 2025))]
    result.to_csv(
        "Cleaned Datasets/Daily Blood Donations by Blood Group.csv", index=False
    )
    print(result)


# To run the functions in terminal : python data_cleaning.py
create_daily_blood_donations()
