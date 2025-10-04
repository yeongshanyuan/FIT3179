import pandas as pd


def create_flow_data_from_hospital_to_state_to_agegroup():
    """
    Create a two-level Sankey dataset showing flow from Hospital → State → Age Group.
    """

    facility_df = pd.read_csv("Original Datasets/New Donors by Facility.csv")

    facility_df = facility_df.dropna(subset=["hospital"])
    facility_df = facility_df[facility_df["hospital"].str.strip() != ""]
    facility_df = facility_df[facility_df["total"] > 0]
    facility_df["hospital"] = facility_df["hospital"].str.strip().str.title()

    facility_df["date"] = pd.to_datetime(facility_df["date"], errors="coerce")
    facility_df["year"] = facility_df["date"].dt.year

    facility_df = facility_df[
        (facility_df["year"] >= 2010) & (facility_df["year"] <= 2024)
    ]

    age_columns = [
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
        "total",
    ]
    facility_df[age_columns] = (
        facility_df[age_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
    )

    hospital_to_state = {
        "Hospital Sultanah Nora Ismail": "Johor",
        "Hospital Sultanah Aminah": "Johor",
        "Hospital Sultanah Bahiyah": "Kedah",
        "Hospital Raja Perempuan Zainab Ii": "Kelantan",
        "Hospital Melaka": "Melaka",
        "Hospital Tuanku Jaafar": "Negeri Sembilan",
        "Hospital Tengku Ampuan Afzan": "Pahang",
        "Hospital Sultan Haji Ahmad Shah": "Pahang",
        "Hospital Seberang Jaya": "Pulau Pinang",
        "Hospital Pulau Pinang": "Pulau Pinang",
        "Hospital Raja Permaisuri Bainun": "Perak",
        "Hospital Taiping": "Perak",
        "Hospital Seri Manjung": "Perak",
        "Hospital Tengku Ampuan Rahimah": "Selangor",
        "Hospital Sultanah Nur Zahirah": "Terengganu",
        "Hospital Queen Elizabeth Ii": "Sabah",
        "Hospital Duchess Of Kent": "Sabah",
    }

    facility_df = facility_df.copy()
    facility_df["state"] = facility_df["hospital"].map(hospital_to_state)
    facility_df = facility_df.dropna(subset=["state"])

    sankey_df = facility_df.melt(
        id_vars=["year", "state", "hospital"],
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
        var_name="age_group",
        value_name="donors",
    )

    sankey_df = sankey_df[sankey_df["donors"] > 0]
    sankey_df = sankey_df.groupby(
        ["year", "hospital", "state", "age_group"], as_index=False
    )["donors"].sum()
    sankey_df.rename(
        columns={
            "year": "Year",
            "hospital": "Hospital",
            "state": "State",
            "age_group": "Age Group",
            "donors": "New Donors",
        },
        inplace=True,
    )

    sankey_df.to_csv("Cleaned Datasets/New Donors Flow.csv", index=False)
    print(sankey_df)


# To run the function in terminal : python "Data Transformation/data_cleaning_new_donors.py"
create_flow_data_from_hospital_to_state_to_agegroup()
