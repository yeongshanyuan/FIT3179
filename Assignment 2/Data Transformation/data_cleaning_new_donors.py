import pandas as pd


def create_flow_data_from_hospital_to_state_to_agegroup():
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
        "Hospital Tawau": "Sabah",
        "Hospital Umum Sarawak": "Sarawak",
        "Hospital Miri": "Sarawak",
    }

    facility_df["state"] = facility_df["hospital"].map(hospital_to_state)
    facility_df = facility_df.dropna(subset=["state"])

    sankey_df = facility_df.melt(
        id_vars=["year", "state", "hospital"],
        value_vars=age_columns,
        var_name="age_group",
        value_name="donors",
    )

    sankey_df = sankey_df[sankey_df["donors"] > 0]
    sankey_df = sankey_df.groupby(
        ["year", "hospital", "state", "age_group"], as_index=False
    )["donors"].sum()

    hospital_state = (
        sankey_df.groupby(["year", "hospital", "state"])["donors"].sum().reset_index()
    )
    hospital_state.columns = ["year", "source", "target", "value"]

    state_age = (
        sankey_df.groupby(["year", "state", "age_group"])["donors"].sum().reset_index()
    )
    state_age.columns = ["year", "source", "target", "value"]

    sankey_flow = pd.concat([hospital_state, state_age], ignore_index=True)

    sankey_flow.to_csv("Cleaned Datasets/New Donors Sankey Flow.csv", index=False)
    print(sankey_flow)


# To run the functions in terminal : python "Data Transformation\data_cleaning_new_donors.py"
create_flow_data_from_hospital_to_state_to_agegroup()
