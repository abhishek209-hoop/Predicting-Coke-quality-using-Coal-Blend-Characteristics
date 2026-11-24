"""
Data Preprocessing Module for Coke Quality Prediction Project.
Performs data ingestion, column mapping, quality checks (missing values, duplicates,
TR+TI compositional constraint, outlier identification), and rigorous 80/20 train/test split.
"""

import sys
from pathlib import Path
import pandas as pd
# pyrefly: ignore[missing-import]
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# pyrefly: ignore[missing-import]
import joblib

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config


def load_raw_data(raw_path=config.RAW_DATA_PATH):
    """
    Loads raw CSV data containing multi-level headers.
    Returns cleaned DataFrame with explicit Serial_No and standardized column names.
    """
    raw_path = Path(raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {raw_path}")

    # The raw file has group headers on line 0 and column names on line 1
    # Line 2 onwards contains data where first column is serial number
    df = pd.read_csv(raw_path, header=1)
    
    # Reset index to create explicit Serial_No column if index was serial number
    df.index.name = "Serial_No"
    df = df.reset_index()

    # Clean column names and map to standard names
    renamed_cols = {}
    for col in df.columns:
        clean_col = col.strip()
        matched = False
        for raw_k, std_v in config.COLUMN_MAPPING.items():
            if raw_k.lower() == clean_col.lower() or raw_k.replace("–", "-") == clean_col.replace("–", "-"):
                renamed_cols[col] = std_v
                matched = True
                break
        if not matched and col != "Serial_No":
            renamed_cols[col] = clean_col

    df = df.rename(columns=renamed_cols)
    return df


def audit_data_quality(df):
    """
    Performs comprehensive data quality audit:
    - Missing values count & percentage
    - Exact duplicate rows and duplicate feature rows
    - TR + TI compositional balance check
    - Plausible metallurgical range verification
    - Outlier identification via IQR and Z-scores
    """
    audit = {}

    # Basic dimensions
    audit["n_rows"] = int(len(df))
    audit["n_cols"] = int(df.shape[1])
    audit["columns"] = list(df.columns)
    audit["dtypes"] = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # 1. Missing Values
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100.0
    audit["missing_values"] = pd.DataFrame({
        "Missing_Count": null_counts,
        "Missing_Percentage": null_pct
    })

    # 2. Duplicate Analysis
    audit["exact_duplicates_count"] = int(df.duplicated().sum())
    feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
    dup_features = df.duplicated(subset=feature_cols, keep=False)
    audit["duplicate_feature_combinations_count"] = int(dup_features.sum())
    if dup_features.sum() > 0:
        audit["duplicate_feature_rows"] = df[dup_features]
    else:
        audit["duplicate_feature_rows"] = pd.DataFrame()

    # 3. Compositional Consistency: TR + TI
    tr_ti_sum = df["TR"] + df["TI"]
    audit["tr_ti_sum_stats"] = {
        "mean": float(tr_ti_sum.mean()),
        "min": float(tr_ti_sum.min()),
        "max": float(tr_ti_sum.max()),
        "std": float(tr_ti_sum.std()),
        "count_exactly_100": int((tr_ti_sum == 100.0).sum()),
        "max_deviation_from_100": float(np.max(np.abs(tr_ti_sum - 100.0)))
    }
    deviating_rows = df[np.abs(tr_ti_sum - 100.0) > 0.05]
    audit["tr_ti_deviating_rows"] = deviating_rows[["Serial_No", "TR", "TI"]]

    # 4. Metallurgical Range Checks
    range_violations = []
    for var, meta in config.FEATURE_METADATA.items():
        if var in df.columns:
            below_min = df[df[var] < meta["min"]]
            above_max = df[df[var] > meta["max"]]
            if len(below_min) > 0 or len(above_max) > 0:
                range_violations.append({
                    "variable": var,
                    "below_min_count": len(below_min),
                    "above_max_count": len(above_max)
                })
    audit["range_violations"] = range_violations

    # 5. Outlier Detection (Univariate IQR)
    outliers = {}
    for col in config.STANDARDIZED_FEATURE_COLUMNS + config.TARGET_COLUMNS:
        q25 = df[col].quantile(0.25)
        q75 = df[col].quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outlier_rows = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outliers[col] = {
            "q25": float(q25),
            "q75": float(q75),
            "iqr": float(iqr),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "n_outliers": len(outlier_rows),
            "outlier_serials": outlier_rows["Serial_No"].tolist(),
            "outlier_values": outlier_rows[col].tolist()
        }
    audit["iqr_outliers"] = outliers

    # 6. Specific Dash et al. (2012) Anomalous Observations Investigation
    # Observation #11 (extremely low CSR=18.8, high CRI=52.0)
    # Observation #10 (low V9-V13=39)
    # Observations #6, 7, 37, 38, 39 (high BI >= 0.23)
    notable_observations = df[df["Serial_No"].isin([6, 7, 10, 11, 15, 37, 38, 39, 46])]
    audit["notable_observations"] = notable_observations

    return audit


def preprocess_and_split(df, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE):
    """
    Performs train/test split (80/20) with fixed random seed.
    Fits StandardScaler on training features strictly to avoid data leakage.
    Saves clean full dataset, train set, and test set.
    """
    feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
    target_cols = config.TARGET_COLUMNS

    # Ensure output directories exist
    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # Clean full dataframe
    df_cleaned = df.copy()

    # Train-test split
    train_df, test_df = train_test_split(
        df_cleaned,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    # Sort by Serial_No for consistency
    train_df = train_df.sort_values(by="Serial_No").reset_index(drop=True)
    test_df = test_df.sort_values(by="Serial_No").reset_index(drop=True)

    # Fit scaler on training set strictly
    scaler = StandardScaler()
    scaler.fit(train_df[feature_cols])

    # Save scaler
    scaler_path = config.PROCESSED_DATA_DIR / "scaler.joblib"
    joblib.dump(scaler, scaler_path)

    # Export datasets
    df_cleaned.to_csv(config.PROCESSED_DATA_DIR / "cleaned_coal_coke.csv", index=False)
    train_df.to_csv(config.PROCESSED_DATA_DIR / "train.csv", index=False)
    test_df.to_csv(config.PROCESSED_DATA_DIR / "test.csv", index=False)

    return {
        "full_df": df_cleaned,
        "train_df": train_df,
        "test_df": test_df,
        "scaler": scaler,
        "feature_cols": feature_cols,
        "target_cols": target_cols
    }


if __name__ == "__main__":
    df = load_raw_data()
    print("Loaded data successfully. Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    audit = audit_data_quality(df)
    print("\n--- Data Audit Summary ---")
    print(f"Total Rows: {audit['n_rows']}, Total Cols: {audit['n_cols']}")
    print(f"Missing Values: {audit['missing_values']['Missing_Count'].sum()}")
    print(f"Exact Duplicates: {audit['exact_duplicates_count']}")
    print(f"TR + TI Mean: {audit['tr_ti_sum_stats']['mean']:.4f}, Max Dev: {audit['tr_ti_sum_stats']['max_deviation_from_100']:.4f}")
    print("\nNotable Observations identified (e.g. Serial #11, #10, #37, etc.):")
    print(audit["notable_observations"][["Serial_No", "Ash", "VM", "Ro", "V9_V13", "BI", "CSR", "CRI"]])

    split_res = preprocess_and_split(df)
    print(f"\nSplits created: Train={len(split_res['train_df'])} rows, Test={len(split_res['test_df'])} rows.")

