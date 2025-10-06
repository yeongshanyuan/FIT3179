import pandas as pd


def get_Singapore_blood_donations_rate():
    """
    Read the Singapore blood donors annual dataset.
    Existing columns: DataSeries, 2010, 2011, ..., 2025.
    Filter out row for Mean Donations Per 1,000 Total Population only.
    Melt the dataframe to have Year and Blood Donations Rate columns.
    """
    df = pd.read_csv("Original Datasets\Singapore Blood Donors Annual.csv")

    df = df[df["DataSeries"] == "Mean Donations Per 1,000 Total Population"]
    df = df.melt(
        id_vars=["DataSeries"],
        var_name="Year",
        value_name="Mean Donations Per 1,000 Total Population",
    )
    df = df.drop(columns=["DataSeries"])
    df["Year"] = df["Year"].astype(int)

    df["Mean Donations Per 1,000 Total Population"] = df[
        "Mean Donations Per 1,000 Total Population"
    ].astype(float)
    df = df.rename(
        columns={"Mean Donations Per 1,000 Total Population": "Blood Donations Rate"}
    )
    return df


def get_Malaysia_populations():
    """
    Read the Malaysia populations dataset.
    Existing columns: date, sex, age, ethnicity, population.
    Filter out rows where sex = both, age = overall, ethnicity = overall.
    Filter dates to be in between 2010 to 2024.
    """
    df = pd.read_csv("Original Datasets\Malaysia Populations.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")
    df = df[df["year"].between(2010, 2024)]

    df = df[
        (df["sex"] == "both")
        & (df["age"] == "overall")
        & (df["ethnicity"] == "overall")
    ]
    df = df.drop(columns=["date", "sex", "age", "ethnicity"])
    df = df.rename(columns={"population": "Population", "year": "Year"})
    return df


def get_Malaysia_blood_donations():
    """
    Read the daily blood donations dataset.
    Existing columns: date, state, blood_type, donations.
    Filter out rows where blood_type is 'all'.
    Filter dates to be in between 2010 to 2024.
    Group by year, summing donations.
    """
    df = pd.read_csv("Original Datasets\Daily Blood Donations by Blood Group.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year.astype("Int64")
    df = df[df["year"].between(2010, 2024)]
    df = df[df["blood_type"] == "all"]

    df = df.groupby("year", as_index=False)["donations"].sum()
    df = df.rename(columns={"donations": "Total Blood Donations", "year": "Year"})
    return df


def get_Malaysia_blood_donations_rate():
    """
    Calculate Malaysia blood donations rate.
    """
    df_donations = get_Malaysia_blood_donations()
    df_population = get_Malaysia_populations()

    # convert to rate first (donations/populations)
    df_new = pd.merge(df_donations, df_population, on="Year", how="inner")
    df_new["Blood Donations Rate"] = (
        df_new["Total Blood Donations"] / df_new["Population"]
    ).round(1)
    df_new = df_new[["Year", "Blood Donations Rate"]]
    return df_new


def create_final_blood_donations_rate():
    """
    Merge Singapore blood donations rate and Malaysia blood donations rate datasets on Year.
    """
    df_sg = get_Singapore_blood_donations_rate()
    df_my = get_Malaysia_blood_donations_rate()

    result = pd.merge(
        df_sg, df_my, on="Year", how="outer", suffixes=("_Singapore", "_Malaysia")
    )
    result.to_csv(
        "Cleaned Datasets/Singapore and Malaysia Blood Donations Rate.csv", index=False
    )
    print(result)


# To run in terminal: python "Data Transformation\data_cleaning_country_blood_donations_comparison.py"
create_final_blood_donations_rate()
