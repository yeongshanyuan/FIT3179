import pandas as pd


def create_daily_blood_donations():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter rows where blood_type is not 'all'.
    Filter dates to be in between 2010 to 2024.
    Save the cleaned dataset.
    """
    df = pd.read_csv("Original Datasets/Daily Blood Donations by Blood Group.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["blood_type"] = df["blood_type"].str.upper()

    result = df[(df["blood_type"] != "ALL") & (df["date"].dt.year.between(2010, 2024))]
    result.rename(
        columns={"date": "Date", "blood_type": "Blood Type", "donations": "Donations"},
        inplace=True,
    )

    result.to_csv(
        "Cleaned Datasets/Daily Blood Donations by Blood Group.csv", index=False
    )
    print(result)


def create_daily_blood_donations_all():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter rows where blood_type is 'all'.
    Filter dates to be in between 2010 to 2024.
    Save the cleaned dataset.
    """
    df = pd.read_csv("Original Datasets/Daily Blood Donations by Blood Group.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    result = df[(df["blood_type"] == "all") & (df["date"].dt.year.between(2010, 2025))]
    result.rename(
        columns={"date": "Date", "blood_type": "Blood Type", "donations": "Donations"},
        inplace=True,
    )

    result.to_csv("Cleaned Datasets/Daily Blood Donations.csv", index=False)
    print(result)


# To run the functions in terminal : python "Data Transformation\data_cleaning_daily_blood_type_donations.py"
create_daily_blood_donations()
create_daily_blood_donations_all()
