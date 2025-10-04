import pandas as pd


def create_yearly_blood_donations_by_state():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter out rows where blood_type is 'all'.
    Filter dates to be in between 2010 and 2025.
    Group by year and state, summing donations.
    """
    df = pd.read_csv(
        "Original Datasets/Daily Blood Donations by Blood Group and State.csv"
    )
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")

    df = df[(df["blood_type"].str.lower() == "all") & (df["year"].between(2010, 2025))]

    result = df.groupby(["year", "state"], as_index=False)["donations"].sum()
    return result


def create_yearly_new_donors_by_state():
    """
    Read the daily new donors dataset.
    Existing columns: date, state, 17-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, other, total
    Filter dates to be in between 2010 and 2025.
    Group by state, summing total new donors.
    """
    df = pd.read_csv("Original Datasets/New Donors by State.csv")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")
    df = df[df["year"].between(2010, 2025)]
    df = df[df["state"] != "Malaysia"]

    result = df.groupby(["year", "state"], as_index=False)["total"].sum()
    return result


def merge_blood_donations_and_new_donors():
    """
    Merge blood donations and new donors datasets on state.
    Adjust state names for consistency.
    """
    df_nd = create_yearly_new_donors_by_state()
    df_bd = create_yearly_blood_donations_by_state()

    state_map = {
        "Negeri Sembilan": "NegeriSembilan",
        "Pulau Pinang": "PulauPinang",
        "Terengganu": "Trengganu",
        "W.P. Kuala Lumpur": "KualaLumpur",
    }
    df_nd["state"] = df_nd["state"].replace(state_map)
    df_bd["state"] = df_bd["state"].replace(state_map)

    df_merged = pd.merge(df_nd, df_bd, on=["year", "state"], how="outer")

    # Add missing 
    additional_states = ["Labuan", "Putrajaya", "Perlis"]
    for state in additional_states:
        for year in range(2010, 2026):
            df_merged = pd.concat(
                [
                    df_merged,
                    pd.DataFrame(
                        [{"year": year, "state": state, "total": -1, "donations": -1}]
                    ),
                ],
                ignore_index=True,
            )

    # Rename the column 
    df_merged = df_merged.rename(
        columns={
            "state": "State",
            "total": "Total New Donors",
            "donations": "Total Blood Donations",
            "year": "Year",
        }
    )

    df_merged.to_csv(
        "Cleaned Datasets/New Donors and Total Blood Donations 2010-2025.csv",
        index=False,
    )
    print(df_merged)


# To run in terminal: python "Data Transformation\data_cleaning_new_donors_in_total_blood_distribution.py"
merge_blood_donations_and_new_donors()
