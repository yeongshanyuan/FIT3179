import pandas as pd

def create_daily_blood_donations():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter out rows where blood_type is 'all'.
    Filter dates to be in the year 2024.
    Save the cleaned dataset.
    """
    df = pd.read_csv("Original Datasets/Daily Blood Donations by Blood Group.csv")
    df["date"] = pd.to_datetime(df["date"])
    df_filtered = df[
        (df["blood_type"] != "all") &
        (df["date"].dt.year == 2024)]
    
    df_filtered.to_csv("Cleaned Datasets/Daily Blood Donations by Blood Group.csv", index=False)
    print(df_filtered)

def create_yearly_blood_donations_by_state():
    """
    Read the daily blood donations dataset. 
    Existing columns: date, state, blood_type, donations. 
    Filter 2024 data and set blood_type to 'all'. 
    Group by year and state, summing donations.
    """
    df = pd.read_csv("Original Datasets/Daily Blood Donations by Blood Group and State.csv")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")
    df = df[df["blood_type"].str.lower() == "all"]
    df = df[df["year"] == 2024]

    result = df.groupby(["year", "state"], as_index=False)["donations"].sum()
    result = result[["state", "donations"]]
    result.to_csv("Cleaned Datasets/Blood Donations by State 2024.csv", index=False)

    print(result)

def create_yearly_new_donors_by_state():
    """
    Read the daily new donors dataset.
    Existing columns: date, state, 17-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, other, total
    Filter 2024 data. 
    Group by state, summing total new donors.
    """
    df = pd.read_csv("Original Datasets/Daily New Donors by State.csv")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")
    df_2024 = df[df["year"] == 2024]

    result = df_2024.groupby("state", as_index=False)["total"].sum()
    result.to_csv("Cleaned Datasets/New Donors by State 2024.csv", index=False)

    print(result)

def merge_blood_donations_and_new_donors():
    """
    Merge the 2024 blood donations and new donors datasets on state.
    Adjust state names for consistency.
    """
    df_nd = pd.read_csv("Cleaned Datasets/New Donors by State 2024.csv")
    df_bd = pd.read_csv("Cleaned Datasets/Blood Donations by State 2024.csv")

    state_map = {
        "Negeri Sembilan": "NegeriSembilan",
        "Pulau Pinang": "PulauPinang",
        "Terengganu": "Trengganu",
        "W.P. Kuala Lumpur": "KualaLumpur"
    }

    df_nd["state"] = df_nd["state"].replace(state_map)
    df_bd["state"] = df_bd["state"].replace(state_map)
    df_merged = pd.merge(df_nd, df_bd, on=["state"], how="inner")

    additional_states = ["Labuan", "Putrajaya", "Perlis"]
    for state in additional_states:
        df_merged = pd.concat([df_merged, pd.DataFrame([{"state": state, "total": -1, "donations": -1}])], ignore_index=True)
    
    df_merged = df_merged.rename(columns={"state": "State", "total": "Total New Donors", "donations": "Total Blood Donations", "year": "Year"})
    df_merged.to_csv("Cleaned Datasets/New Donors and Total Blood Donations 2024.csv", index=False)

    print(df_merged)


# To run the functions in terminal : python data_cleaning.py
create_daily_blood_donations()

create_yearly_blood_donations_by_state()
create_yearly_new_donors_by_state()
merge_blood_donations_and_new_donors()
