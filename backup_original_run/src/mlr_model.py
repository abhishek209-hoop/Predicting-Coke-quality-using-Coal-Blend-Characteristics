"""
Multiple Linear Regression (MLR) Phase 1 Module.
Reproduces the full 8-variable baseline MLR methodology.
Fits independent OLS models for CSR and CRI, diagnoses multicollinearity and compositional closure (TR+TI),
extracts coefficients, p-values, confidence intervals, and calculates CV and test metrics.
"""

import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_predict
# pyrefly: ignore[missing-import]
import joblib

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config
from src.evaluation import calculate_regression_metrics


def fit_and_evaluate_mlr(train_df, test_df, target="CSR", feature_cols=None):
    """
    Fits statsmodels OLS and sklearn LinearRegression using all 8 features.
    Computes cross-validation, training, and test metrics.
    
    Parameters:
    -----------
    train_df : pd.DataFrame
        Training data.
    test_df : pd.DataFrame
        Untouched test data.
    target : str, default="CSR"
        Target column name ("CSR" or "CRI").
    feature_cols : list, optional
        List of feature column names.
        
    Returns:
    --------
    dict containing fitted models, summaries, metrics, and prediction arrays.
    """
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS

    X_train = train_df[feature_cols].values
    y_train = train_df[target].values
    X_test = test_df[feature_cols].values
    y_test = test_df[target].values

    # 1. Statsmodels OLS for in-depth statistical inference
    X_train_sm = sm.add_constant(train_df[feature_cols])
    X_test_sm = sm.add_constant(test_df[feature_cols])
    ols_model = sm.OLS(y_train, X_train_sm).fit()

    # 2. Sklearn LinearRegression for consistent ML workflow and cross-validation
    sklearn_model = LinearRegression(fit_intercept=True)
    sklearn_model.fit(X_train, y_train)

    # 3. Cross-Validation (5-fold) strictly on training set
    kf = KFold(n_splits=config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE)
    cv_preds = cross_val_predict(sklearn_model, X_train, y_train, cv=kf)
    
    cv_rmse_scores = []
    cv_r2_scores = []
    for tr_idx, val_idx in kf.split(X_train):
        m = LinearRegression(fit_intercept=True)
        m.fit(X_train[tr_idx], y_train[tr_idx])
        p_val = m.predict(X_train[val_idx])
        cv_rmse_scores.append(np.sqrt(np.mean((y_train[val_idx] - p_val) ** 2)))
        # R2
        ss_res = np.sum((y_train[val_idx] - p_val) ** 2)
        ss_tot = np.sum((y_train[val_idx] - np.mean(y_train[val_idx])) ** 2)
        cv_r2_scores.append(1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0)

    # Predictions
    train_preds = sklearn_model.predict(X_train)
    test_preds = sklearn_model.predict(X_test)

    # Calculate metrics
    train_metrics = calculate_regression_metrics(y_train, train_preds, n_features=len(feature_cols), prefix="train_")
    test_metrics = calculate_regression_metrics(y_test, test_preds, n_features=len(feature_cols), prefix="test_")

    cv_mean_r2 = float(np.mean(cv_r2_scores))
    cv_std_r2 = float(np.std(cv_r2_scores))
    cv_mean_rmse = float(np.mean(cv_rmse_scores))
    cv_std_rmse = float(np.std(cv_rmse_scores))

    # Compile coefficients summary table
    conf_int = ols_model.conf_int()
    coef_df = pd.DataFrame({
        "Variable": X_train_sm.columns,
        "Coefficient": ols_model.params.values,
        "Std_Error": ols_model.bse.values,
        "t_Statistic": ols_model.tvalues.values,
        "p_Value": ols_model.pvalues.values,
        "CI_Lower_95%": conf_int[0].values,
        "CI_Upper_95%": conf_int[1].values
    }).set_index("Variable")

    # Readable mathematical equation string
    intercept = ols_model.params["const"]
    eq_parts = [f"{intercept:.4f}"]
    for feat in feature_cols:
        coef = ols_model.params[feat]
        sign = "+" if coef >= 0 else "-"
        eq_parts.append(f"{sign} {abs(coef):.4f}*({feat})")
    equation_str = f"{target} = " + " ".join(eq_parts)

    # Save models
    target_dir = config.MODELS_CSR_DIR if target == "CSR" else config.MODELS_CRI_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(sklearn_model, target_dir / "mlr_model.joblib")

    # Save statsmodels summary text
    with open(target_dir / "mlr_statsmodels_summary.txt", "w") as f:
        f.write(ols_model.summary().as_text())
        f.write("\n\nMathematical Equation:\n" + equation_str + "\n")

    return {
        "target": target,
        "ols_model": ols_model,
        "sklearn_model": sklearn_model,
        "coef_df": coef_df,
        "equation_str": equation_str,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "cv_metrics": {
            "cv_mean_r2": cv_mean_r2,
            "cv_std_r2": cv_std_r2,
            "cv_mean_rmse": cv_mean_rmse,
            "cv_std_rmse": cv_std_rmse
        },
        "train_preds": train_preds,
        "cv_preds": cv_preds,
        "test_preds": test_preds,
        "y_train": y_train,
        "y_test": y_test
    }


def run_mlr_phase1():
    """
    Runs MLR Phase 1 for both CSR and CRI, outputs results, and exports tables.
    """
    train_df = pd.read_csv(config.PROCESSED_DATA_DIR / "train.csv")
    test_df = pd.read_csv(config.PROCESSED_DATA_DIR / "test.csv")

    csr_res = fit_and_evaluate_mlr(train_df, test_df, target="CSR")
    cri_res = fit_and_evaluate_mlr(train_df, test_df, target="CRI")

    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)

    csr_res["coef_df"].to_csv(config.TABLES_DIR / "mlr_csr_coefficients.csv")
    csr_res["coef_df"].to_excel(config.TABLES_DIR / "mlr_csr_coefficients.xlsx")

    cri_res["coef_df"].to_csv(config.TABLES_DIR / "mlr_cri_coefficients.csv")
    cri_res["coef_df"].to_excel(config.TABLES_DIR / "mlr_cri_coefficients.xlsx")

    # Combine coefficients into single comparative table
    combined_coef = pd.DataFrame({
        "CSR_Coefficient": csr_res["coef_df"]["Coefficient"],
        "CSR_p_value": csr_res["coef_df"]["p_Value"],
        "CRI_Coefficient": cri_res["coef_df"]["Coefficient"],
        "CRI_p_value": cri_res["coef_df"]["p_Value"]
    })
    combined_coef.to_csv(config.TABLES_DIR / "mlr_combined_coefficients.csv")
    combined_coef.to_excel(config.TABLES_DIR / "mlr_combined_coefficients.xlsx")

    return {"CSR": csr_res, "CRI": cri_res}


if __name__ == "__main__":
    res = run_mlr_phase1()
    print("=== CSR MLR Equation ===")
    print(res["CSR"]["equation_str"])
    print("\nCSR Metrics:")
    print(f"Train R2: {res['CSR']['train_metrics']['train_R2']:.4f}, Train Adj R2: {res['CSR']['train_metrics']['train_Adj_R2']}")
    print(f"CV R2: {res['CSR']['cv_metrics']['cv_mean_r2']:.4f} +/- {res['CSR']['cv_metrics']['cv_std_r2']:.4f}")
    print(f"Test R2: {res['CSR']['test_metrics']['test_R2']:.4f}, Test RMSE: {res['CSR']['test_metrics']['test_RMSE']:.4f}")

    print("\n=== CRI MLR Equation ===")
    print(res["CRI"]["equation_str"])
    print("\nCRI Metrics:")
    print(f"Train R2: {res['CRI']['train_metrics']['train_R2']:.4f}, Train Adj R2: {res['CRI']['train_metrics']['train_Adj_R2']}")
    print(f"CV R2: {res['CRI']['cv_metrics']['cv_mean_r2']:.4f} +/- {res['CRI']['cv_metrics']['cv_std_r2']:.4f}")
    print(f"Test R2: {res['CRI']['test_metrics']['test_R2']:.4f}, Test RMSE: {res['CRI']['test_metrics']['test_RMSE']:.4f}")

