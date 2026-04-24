# ======================================================
# Import libraries
# ======================================================
import pandas as pd
import os

# ======================================================
# Load raw dataset
# ======================================================
raw_data_2026 = pd.read_csv("Data_Files/raw_data_2026.csv")
race_starts = pd.read_csv("Data_Files/race_starts.csv")
laps_completed = pd.read_csv("Data_Files/laps_completed.csv")

# ======================================================
# Create composite row identifier
# ======================================================

def process_id_column(df, id_cols):
    df = df.copy()
    
    df["ID"] = df[id_cols].astype(str).agg("_".join, axis=1)
    df = df.drop(columns=id_cols)
    df = df[["ID"] + [col for col in df.columns if col != "ID"]]
    
    return df

# Apply to raw data set
id_cols = ["Constructor_Lineage_ID", "Season", "Team_Name"]
raw_data_2026 = process_id_column(raw_data_2026, id_cols)

# ======================================================
#  Driver-Level Features from Supplementary Data:
# - `Driver_Lineup_Total_Race_Starts`
# - `Driver_Lineup_3_Season_Race_Starts`
# - `Driver_Lineup_Total_Laps_Completed`
# - `Driver_Lineup_3_Season_Laps_Completed`
# ======================================================

# ------------------------------------------------------
# 1) Reshape driver stat tables
# ------------------------------------------------------
race_starts_long = race_starts.melt(
    id_vars="Driver",
    var_name="Year",
    value_name="Race_Starts"
)

laps_long = laps_completed.melt(
    id_vars="Driver",
    var_name="Year",
    value_name="Laps_Completed"
)

race_starts_long["Year"] = race_starts_long["Year"].astype(int)
laps_long["Year"] = laps_long["Year"].astype(int)

# ------------------------------------------------------
# 2) Extract Season from ID
# ------------------------------------------------------
raw_data_2026 = raw_data_2026.copy()
raw_data_2026["Season"] = raw_data_2026["ID"].str.split("_").str[1].astype(int)

# ------------------------------------------------------
# 3) Feature configuration
# ------------------------------------------------------
features = [
    ("Race_Starts", race_starts_long),
    ("Laps_Completed", laps_long)
]

driver_cols = ["Driver_A", "Driver_B"]

# output containers
results = {
    "A_total": {},
    "B_total": {},
    "A_3s": {},
    "B_3s": {}
}

# ------------------------------------------------------
# 4) Feature engineering loop
# ------------------------------------------------------
for value_col, stat_long in features:

    for driver_prefix in ["A", "B"]:

        driver_col = f"Driver_{driver_prefix}"

        # -------------------------
        # TOTAL (career)
        # -------------------------
        tmp = raw_data_2026.merge(
            stat_long,
            left_on=driver_col,
            right_on="Driver",
            how="left"
        )

        tmp_total = tmp[tmp["Year"] < tmp["Season"]]
        total = tmp_total.groupby("ID")[value_col].sum()

        results[f"{driver_prefix}_total"][value_col] = total

        # -------------------------
        # Prior 3 Seasons
        # -------------------------
        tmp_3s = tmp[
            (tmp["Year"] < tmp["Season"]) &
            (tmp["Year"] >= tmp["Season"] - 3)
        ]

        window_3s = tmp_3s.groupby("ID")[value_col].sum()

        results[f"{driver_prefix}_3s"][value_col] = window_3s

# ------------------------------------------------------
# 5) Build final dataframe
# ------------------------------------------------------
df = raw_data_2026.copy()

df["Driver_Lineup_Total_Race_Starts"] = (
    results["A_total"]["Race_Starts"].reindex(df["ID"]).fillna(0).values +
    results["B_total"]["Race_Starts"].reindex(df["ID"]).fillna(0).values
)

df["Driver_Lineup_3_Season_Race_Starts"] = (
    results["A_3s"]["Race_Starts"].reindex(df["ID"]).fillna(0).values +
    results["B_3s"]["Race_Starts"].reindex(df["ID"]).fillna(0).values
)

df["Driver_Lineup_Total_Laps_Completed"] = (
    results["A_total"]["Laps_Completed"].reindex(df["ID"]).fillna(0).values +
    results["B_total"]["Laps_Completed"].reindex(df["ID"]).fillna(0).values
)

df["Driver_Lineup_3_Season_Laps_Completed"] = (
    results["A_3s"]["Laps_Completed"].reindex(df["ID"]).fillna(0).values +
    results["B_3s"]["Laps_Completed"].reindex(df["ID"]).fillna(0).values
)

# ------------------------------------------------------
# 6) Drop columns used for feature engineering
# ------------------------------------------------------
df = df.drop(columns=["Driver_A", "Driver_B", "Season"])

raw_data_2026 = df
raw_data_2026.columns

# ==========================================================
# Create Prior Season Points Proportion
# ==========================================================

def create_prior_season_points_prop(df):
    df = df.copy()

    # Avoid division by zero
    df["Prior_Season_Points_Prop"] = (
        df["Prior_Season_Points_Earned"] /
        df["Prior_Season_Points_Total"]
    ).replace([float("inf"), -float("inf")], 0)

    # Handle NaN values and clip to [0, 1]
    df["Prior_Season_Points_Prop"] = df["Prior_Season_Points_Prop"].fillna(0)
    df["Prior_Season_Points_Prop"] = df["Prior_Season_Points_Prop"].clip(0, 1)

    # Drop original columns
    df = df.drop(
        columns=[
            "Prior_Season_Points_Earned",
            "Prior_Season_Points_Total"
        ]
    )

    return df

# Apply to raw data set
raw_data_2026 = create_prior_season_points_prop(raw_data_2026)

# ==========================================================
# Create Prior Season Win Proportion
# ==========================================================

def create_prior_season_win_prop(df):
    df = df.copy()

    # Avoid division by zero
    df["Prior_Season_Win_Prop"] = (
        df["Prior_Season_Grand_Prix_Wins"] /
        df["Prior_Season_GP_Count"]
    ).replace([float("inf"), -float("inf")], 0)

    # Handle NaN values and clip to [0, 1]
    df["Prior_Season_Win_Prop"] = df["Prior_Season_Win_Prop"].fillna(0)
    df["Prior_Season_Win_Prop"] = df["Prior_Season_Win_Prop"].clip(0, 1)

    # Drop original columns
    df = df.drop("Prior_Season_Grand_Prix_Wins")

    return df

# Apply to raw data set
raw_data_2026 = create_prior_season_win_prop(raw_data_2026)

# ============================================================================
# Create Proportion of Previous 3 Season Race Starts for the Driver Lineup
# ============================================================================

def create_driver_lineup_3_season_race_start_prop(df):
    df = df.copy()

    # Avoid division by zero
    df["Driver_Lineup_3_Season_Race_Start_Prop"] = (
        df["Driver_Lineup_3_Season_Race_Starts"] /
        (df["Prior_3_Season_GP_Count"] * 2))

    # Handle NaN values and clip to [0, 1]
    df["Driver_Lineup_3_Season_Race_Start_Prop"] = df["Driver_Lineup_3_Season_Race_Start_Prop"].fillna(0)
    df["Driver_Lineup_3_Season_Race_Start_Prop"] = df["Driver_Lineup_3_Season_Race_Start_Prop"].clip(0, 1)

    # Drop original columns
    df = df.drop(
        columns=[
            "Driver_Lineup_3_Season_Race_Starts",
            "Prior_3_Season_GP_Count"
        ]
    )

    return df

# Apply to raw data set
raw_data_2026 = create_driver_lineup_3_season_race_start_prop(raw_data_2026)

# ============================================================================
# Create Proportion of Laps Driven in Previous 3 Seasons for the Driver Lineup
# ============================================================================

def create_driver_lineup_3_season_laps_prop(df):
    df = df.copy()

    # Avoid division by zero
    df["Driver_Lineup_3_Season_Laps_Prop"] = (
        df["Driver_Lineup_3_Season_Laps_Completed"] /
        (df["Prior_3_Season_Lap_Count"] * 2))

    # Handle NaN values and clip to [0, 1]
    df["Driver_Lineup_3_Season_Laps_Prop"] = df["Driver_Lineup_3_Season_Laps_Prop"].fillna(0)
    df["Driver_Lineup_3_Season_Laps_Prop"] = df["Driver_Lineup_3_Season_Laps_Prop"].clip(0, 1)

    # Drop original columns
    df = df.drop(
        columns=[
            "Driver_Lineup_3_Season_Laps_Completed",
            "Prior_3_Season_Lap_Count"
        ]
    )

    return df

# Apply to raw data set
raw_data_2026 = create_driver_lineup_3_season_laps_prop(raw_data_2026)

# ==========================================================
# Create Prior Season Fastest Lap Proportion
# ==========================================================

def create_prior_season_win_prop(df):
    df = df.copy()

    # Avoid division by zero
    df["Prior_Season_Fastest_Lap_Prop"] = (
        df["Prior_Season_Fastest_Lap_Count"] /
        df["Prior_Season_GP_Count"]
    ).replace([float("inf"), -float("inf")], 0)

    # Handle NaN values and clip to [0, 1]
    df["Prior_Season_Fastest_Lap_Prop"] = df["Prior_Season_Fastest_Lap_Prop"].fillna(0)
    df["Prior_Season_Fastest_Lap_Prop"] = df["Prior_Season_Fastest_Lap_Prop"].clip(0, 1)

    # Drop original columns
    df = df.drop(
        columns=[
            "Prior_Season_Fastest_Lap_Count",
            "Prior_Season_GP_Count"
        ]
    )

    return df

# Apply to raw data set
raw_data_2026 = create_prior_season_win_prop(raw_data_2026)

# ==========================================================
# Simplify Engine Branding
# ==========================================================

def simplify_engine_branding(df, col="Engine_Branding"):
    df = df.copy()

    keep_brands = {"FERRARI", "MERCEDES", "HONDA", "FORD"}

    df[col] = (
        df[col]
        .fillna("Other")
        .astype(str)
        .str.upper()
    )

    df[col] = df[col].where(df[col].isin(keep_brands), "Other")

    return df

# Apply to raw data set
raw_data_2026 = simplify_engine_branding(raw_data_2026)

# ======================================================
# Split data into train and test sets (for 2026)
# ======================================================

train = raw_data_2026[raw_data_2026['Season'] != 2026].copy()
test  = raw_data_2026[raw_data_2026['Season'] == 2026].copy()

# ======================================================
# Write processed datasets to CSV
# ======================================================

output_dir = "Data_Files"
os.makedirs(output_dir, exist_ok=True)

train.to_csv(os.path.join(output_dir, "Train.csv"), index=False)
test.to_csv(os.path.join(output_dir, "Test.csv"), index=False)

print(f"Train and Test datasets saved to '{output_dir}' folder.")