# ======================================================
# Import libraries
# ======================================================
import pandas as pd

# ======================================================
# Load raw dataset
# ======================================================

raw_data_2026 = pd.read_csv("raw_data_2026.csv")

# ======================================================
# Split into train and test
# ======================================================

train = raw_data_2026[raw_data_2026['Season'] != 2026].copy()
test  = raw_data_2026[raw_data_2026['Season'] == 2026].copy()

# ======================================================
# Create composite identifier for constructor-season
# ======================================================

def process_id_column(df, id_cols):
    df = df.copy()
    
    # Create composite ID
    df["ID"] = df[id_cols].astype(str).agg("_".join, axis=1)
    
    # Drop original ID columns
    df = df.drop(columns=id_cols)
    
    # Move ID to front
    df = df[["ID"] + [col for col in df.columns if col != "ID"]]
    
    return df

# Columns used for ID
old_id_cols = ["Constructor_Lineage_ID", "Season", "Team_Name"]

# Apply ID processing
train = process_id_column(train, old_id_cols)
test = process_id_column(test, old_id_cols)
