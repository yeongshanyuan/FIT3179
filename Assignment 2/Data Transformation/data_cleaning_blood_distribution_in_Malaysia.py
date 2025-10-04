import pandas as pd


def get_Malaysia_blood_distribution():
    """
    Read the blood type by country in 2025 dataset.
    Filter out row for Malaysia only.
    """
    df = pd.read_csv("Original Datasets\Blood Type by Country 2025.csv")
    df = df[df["country"] == "Malaysia"]

    result = pd.DataFrame(
        {
            "O_Total": df["BloodType_OPosPctOfPop_pct_YearFree"].values
            + df["BloodType_ONegPctOfPop_pct_YearFree"].values,
            "A_Total": df["BloodType_APosPctOfPop_pct_YearFree"].values
            + df["BloodType_ANegPctOfPop_pct_YearFree"].values,
            "B_Total": df["BloodType_BPosPctOfPop_pct_YearFree"].values
            + df["BloodType_BNegPctOfPop_pct_YearFree"].values,
            "AB_Total": df["BloodType_ABPosPctOfPop_pct_YearFree"].values
            + df["BloodType_ABNegPctOfPop_pct_YearFree"].values,
        }
    )

    result.to_csv(
        "Cleaned Datasets/Malaysia Blood Distribution in 2025.csv", index=False
    )
    print(result)


# To run the functions in terminal : python "Data Transformation\data_cleaning_blood_distribution_in_Malaysia.py"
get_Malaysia_blood_distribution()
