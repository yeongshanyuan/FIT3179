import pandas as pd

import pandas as pd


def create_new_donors_by_state_and_age_group():
    """
    Read the new donors by state dataset.
    Existing columns: date, state, 17-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, other.
    Filter out rows where state is Malaysia.
    Filter dates to be in between 2010 to 2024.
    """
    df = pd.read_csv("Original Datasets/New Donors by State.csv")
    df = df[df["state"] != "Malaysia"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    result = df.melt(
        id_vars=["date", "state"],
        value_vars=[
            "17-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "other",
        ],
        var_name="Age Group",
        value_name="Total Blood Donations",
    )

    result["Year"] = result["date"].dt.year
    result = result[result["Year"].between(2010, 2024)]

    result = (
        result.groupby(["Year", "state", "Age Group"], as_index=False)[
            "Total Blood Donations"
        ]
        .sum()
        .rename(columns={"state": "State"})
    )

    result.to_csv("Cleaned Datasets/New Donors by State and Age Group.csv", index=False)
    print(result)


# To run the functions in terminal : python "Data Transformation\data_cleaning_new_donors_by_state_and_age_group.py"
create_new_donors_by_state_and_age_group()
