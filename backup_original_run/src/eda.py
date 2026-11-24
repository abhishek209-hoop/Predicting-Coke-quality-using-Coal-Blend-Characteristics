"""
Exploratory Data Analysis (EDA) Module for Coke Quality Prediction.
Performs descriptive statistical profiling, correlation analysis (Pearson & Spearman),
multicollinearity diagnostics (VIF, condition number, rank), and exports tabular reports.
"""

import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
from statsmodels.stats.outliers_influence import variance_inflation_factor
# pyrefly: ignore[missing-import]
from statsmodels.tools.tools import add_constant

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config


def generate_descriptive_statistics(df, feature_cols=None, target_cols=None):
    """
    Computes comprehensive descriptive statistics including:
    mean, std, median, min, max, 25%, 75%, IQR, skewness, and kurtosis.
    """
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
    if target_cols is None:
        target_cols = config.TARGET_COLUMNS

    all_cols = feature_cols + target_cols
    subset = df[all_cols]

    stats_df = pd.DataFrame(index=all_cols)
    stats_df["Count"] = subset.count()
    stats_df["Mean"] = subset.mean()
    stats_df["Std_Dev"] = subset.std()
    stats_df["Median"] = subset.median()
    stats_df["Min"] = subset.min()
    stats_df["Q25 (25%)"] = subset.quantile(0.25)
    stats_df["Q75 (75%)"] = subset.quantile(0.75)
    stats_df["IQR"] = stats_df["Q75 (75%)"] - stats_df["Q25 (25%)"]
    stats_df["Max"] = subset.max()
    stats_df["Skewness"] = subset.skew()
    stats_df["Kurtosis"] = subset.kurtosis()

    # Add metadata units
    stats_df["Unit"] = [config.FEATURE_METADATA.get(c, {}).get("unit", "") for c in all_cols]
    stats_df["Description"] = [config.FEATURE_METADATA.get(c, {}).get("full_name", "") for c in all_cols]

    # Reorder columns
    cols_order = ["Description", "Unit", "Count", "Mean", "Std_Dev", "Median", "Min", "Q25 (25%)", "Q75 (75%)", "IQR", "Max", "Skewness", "Kurtosis"]
    stats_df = stats_df[cols_order]

    return stats_df


def compute_correlations(df, feature_cols=None, target_cols=None):
    """
    Computes Pearson and Spearman correlation matrices:
    - Full matrix (inputs + targets)
    - Feature vs Feature matrix
    - Feature vs Target matrix
    """
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
    if target_cols is None:
        target_cols = config.TARGET_COLUMNS

    all_cols = feature_cols + target_cols
    subset = df[all_cols]

    pearson_full = subset.corr(method="pearson")
    spearman_full = subset.corr(method="spearman")

    pearson_feat_target = pearson_full.loc[feature_cols, target_cols]
    spearman_feat_target = spearman_full.loc[feature_cols, target_cols]

    pearson_feat_feat = pearson_full.loc[feature_cols, feature_cols]
    spearman_feat_feat = spearman_full.loc[feature_cols, feature_cols]

    return {
        "pearson_full": pearson_full,
        "spearman_full": spearman_full,
        "pearson_feat_target": pearson_feat_target,
        "spearman_feat_target": spearman_feat_target,
        "pearson_feat_feat": pearson_feat_feat,
        "spearman_feat_feat": spearman_feat_feat
    }


def compute_multicollinearity_diagnostics(df, feature_cols=None):
    """
    Calculates Variance Inflation Factor (VIF), condition number,
    matrix rank, and singular values to identify collinearity.
    Special attention paid to the TR + TI compositional relationship.
    """
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS

    X = df[feature_cols].copy()
    X_const = add_constant(X)

    # 1. VIF calculation with constant
    vif_data = []
    for i, col in enumerate(X_const.columns):
        if col == "const":
            continue
        vif_val = variance_inflation_factor(X_const.values, i)
        vif_data.append({
            "Feature": col,
            "VIF_with_constant": float(vif_val),
            "Severity": "Severe Collinearity (VIF > 10)" if vif_val > 10 else ("Moderate Collinearity (5 < VIF <= 10)" if vif_val > 5 else "Low Collinearity (VIF <= 5)")
        })
    vif_df = pd.DataFrame(vif_data).set_index("Feature")

    # 2. VIF without TI (to demonstrate the resolution of the TR-TI dependency)
    features_no_ti = [c for c in feature_cols if c != "TI"]
    X_no_ti = add_constant(df[features_no_ti])
    vif_no_ti_data = []
    for i, col in enumerate(X_no_ti.columns):
        if col == "const":
            continue
        vif_val = variance_inflation_factor(X_no_ti.values, i)
        vif_no_ti_data.append({
            "Feature": col,
            "VIF_without_TI": float(vif_val)
        })
    vif_no_ti_df = pd.DataFrame(vif_no_ti_data).set_index("Feature")

    # Combine VIF analyses
    vif_combined = vif_df.join(vif_no_ti_df)

    # 3. Matrix Rank and Condition Number
    X_vals = X.values
    X_const_vals = X_const.values
    rank_X = np.linalg.matrix_rank(X_vals)
    rank_X_const = np.linalg.matrix_rank(X_const_vals)
    cond_X = np.linalg.cond(X_vals)
    cond_X_const = np.linalg.cond(X_const_vals)
    singular_values = np.linalg.svd(X_const_vals, compute_uv=False)

    collinearity_summary = {
        "n_samples": len(df),
        "n_features": len(feature_cols),
        "design_matrix_rank": int(rank_X_const),
        "max_possible_rank": int(X_const_vals.shape[1]),
        "is_rank_deficient": bool(rank_X_const < X_const_vals.shape[1]),
        "condition_number_with_constant": float(cond_X_const),
        "condition_number_uncentered": float(cond_X),
        "smallest_singular_value": float(singular_values[-1]),
        "largest_singular_value": float(singular_values[0]),
        "tr_ti_correlation": float(df["TR"].corr(df["TI"])),
        "vm_ro_correlation": float(df["VM"].corr(df["Ro"]))
    }

    return {
        "vif_table": vif_combined,
        "collinearity_summary": collinearity_summary
    }


def run_eda_pipeline(df):
    """
    Runs complete EDA pipeline, prints findings, and exports tables to CSV and Excel.
    """
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Descriptive stats
    stats_df = generate_descriptive_statistics(df)
    stats_df.to_csv(config.TABLES_DIR / "descriptive_statistics.csv")
    stats_df.to_excel(config.TABLES_DIR / "descriptive_statistics.xlsx")

    # 2. Correlations
    corr_dict = compute_correlations(df)
    corr_dict["pearson_full"].to_csv(config.TABLES_DIR / "pearson_correlation_matrix.csv")
    corr_dict["spearman_full"].to_csv(config.TABLES_DIR / "spearman_correlation_matrix.csv")
    corr_dict["pearson_feat_target"].to_csv(config.TABLES_DIR / "pearson_feature_target.csv")
    corr_dict["spearman_feat_target"].to_csv(config.TABLES_DIR / "spearman_feature_target.csv")
    
    with pd.ExcelWriter(config.TABLES_DIR / "correlations.xlsx") as writer:
        corr_dict["pearson_full"].to_excel(writer, sheet_name="Pearson_Full")
        corr_dict["spearman_full"].to_excel(writer, sheet_name="Spearman_Full")
        corr_dict["pearson_feat_target"].to_excel(writer, sheet_name="Pearson_Feat_Target")
        corr_dict["spearman_feat_target"].to_excel(writer, sheet_name="Spearman_Feat_Target")

    # 3. Multicollinearity
    mc_res = compute_multicollinearity_diagnostics(df)
    mc_res["vif_table"].to_csv(config.TABLES_DIR / "vif_analysis.csv")
    mc_res["vif_table"].to_excel(config.TABLES_DIR / "vif_analysis.xlsx")

    summary_df = pd.DataFrame(list(mc_res["collinearity_summary"].items()), columns=["Metric", "Value"])
    summary_df.to_csv(config.TABLES_DIR / "collinearity_summary.csv", index=False)
    summary_df.to_excel(config.TABLES_DIR / "collinearity_summary.xlsx", index=False)

    return {
        "stats_df": stats_df,
        "corr_dict": corr_dict,
        "vif_table": mc_res["vif_table"],
        "collinearity_summary": mc_res["collinearity_summary"]
    }


if __name__ == "__main__":
    df = pd.read_csv(config.PROCESSED_DATA_DIR / "cleaned_coal_coke.csv")
    eda_out = run_eda_pipeline(df)
    print("Descriptive Statistics:")
    print(eda_out["stats_df"][["Mean", "Std_Dev", "Median", "Min", "Max", "Skewness"]])
    print("\nPearson Feature-Target Correlations:")
    print(eda_out["corr_dict"]["pearson_feat_target"])
    print("\nVIF Analysis:")
    print(eda_out["vif_table"])
    print("\nCollinearity Summary:")
    for k, v in eda_out["collinearity_summary"].items():
        print(f"  {k}: {v}")

