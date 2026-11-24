"""
XGBoost Regressor Module for Coke Quality Prediction.
Performs 5-fold cross-validation hyperparameter optimization, evaluates CSR and CRI models,
computes feature importances (impurity-based, permutation-based), and generates SHAP values.
"""

import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
import xgboost as xgb
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_val_predict
from sklearn.inspection import permutation_importance
# pyrefly: ignore[missing-import]
import shap
# pyrefly: ignore[missing-import]
import joblib

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config
from src.evaluation import calculate_regression_metrics


def train_xgboost_model(train_df, test_df, target="CSR", feature_cols=None, n_iter=40):
    """
    Trains and tunes an XGBoost Regressor using 5-fold cross-validation on the training set.
    Evaluates generalization on the untouched test set and computes SHAP explanations.
    """
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS

    X_train = train_df[feature_cols].values
    y_train = train_df[target].values
    X_test = test_df[feature_cols].values
    y_test = test_df[target].values

    # Base estimator
    base_xgb = xgb.XGBRegressor(
        objective="reg:squarederror",
        random_state=config.RANDOM_STATE,
        n_jobs=1
    )

    kf = KFold(n_splits=config.CV_FOLDS, shuffle=True, random_state=config.RANDOM_STATE)

    search = RandomizedSearchCV(
        estimator=base_xgb,
        param_distributions=config.XGBOOST_PARAM_GRID,
        n_iter=n_iter,
        scoring="neg_root_mean_squared_error",
        cv=kf,
        random_state=config.RANDOM_STATE,
        n_jobs=1,
        verbose=0
    )

    # Fit hyperparameter optimization strictly on training set
    search.fit(X_train, y_train)
    best_model = search.best_estimator_
    best_params = search.best_params_

    # Cross-validation predictions with best model
    cv_preds = cross_val_predict(best_model, X_train, y_train, cv=kf, n_jobs=1)
    
    cv_rmse_scores = []
    cv_r2_scores = []
    for tr_idx, val_idx in kf.split(X_train):
        m = xgb.XGBRegressor(**best_params, random_state=config.RANDOM_STATE, n_jobs=1)
        m.fit(X_train[tr_idx], y_train[tr_idx])
        p_val = m.predict(X_train[val_idx])
        cv_rmse_scores.append(np.sqrt(np.mean((y_train[val_idx] - p_val) ** 2)))
        ss_res = np.sum((y_train[val_idx] - p_val) ** 2)
        ss_tot = np.sum((y_train[val_idx] - np.mean(y_train[val_idx])) ** 2)
        cv_r2_scores.append(1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0)

    cv_mean_r2 = float(np.mean(cv_r2_scores))
    cv_std_r2 = float(np.std(cv_r2_scores))
    cv_mean_rmse = float(np.mean(cv_rmse_scores))
    cv_std_rmse = float(np.std(cv_rmse_scores))

    # Final fit on all training data
    best_model.fit(X_train, y_train)

    # Predictions
    train_preds = best_model.predict(X_train)
    test_preds = best_model.predict(X_test)

    # Metrics
    train_metrics = calculate_regression_metrics(y_train, train_preds, n_features=len(feature_cols), prefix="train_")
    test_metrics = calculate_regression_metrics(y_test, test_preds, n_features=len(feature_cols), prefix="test_")

    # Feature Importance: Native Impurity / Gain
    feature_importances = pd.Series(best_model.feature_importances_, index=feature_cols).sort_values(ascending=False)

    # Feature Importance: Permutation on Test Set
    perm_importance = permutation_importance(
        best_model, X_test, y_test,
        n_repeats=30,
        random_state=config.RANDOM_STATE,
        scoring="neg_root_mean_squared_error",
        n_jobs=1
    )
    perm_importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Permutation_Importance_Mean": perm_importance.importances_mean,
        "Permutation_Importance_Std": perm_importance.importances_std
    }).sort_values(by="Permutation_Importance_Mean", ascending=False).set_index("Feature")

    # SHAP Values calculation
    explainer = shap.TreeExplainer(best_model)
    shap_values_train = explainer.shap_values(X_train)
    shap_values_test = explainer.shap_values(X_test)

    # Save models
    target_dir = config.MODELS_CSR_DIR if target == "CSR" else config.MODELS_CRI_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, target_dir / "xgboost_model.joblib")

    # Save best parameters to text file
    with open(target_dir / "xgboost_best_params.txt", "w") as f:
        for k, v in best_params.items():
            f.write(f"{k}: {v}\n")

    return {
        "target": target,
        "best_model": best_model,
        "best_params": best_params,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "cv_metrics": {
            "cv_mean_r2": cv_mean_r2,
            "cv_std_r2": cv_std_r2,
            "cv_mean_rmse": cv_mean_rmse,
            "cv_std_rmse": cv_std_rmse
        },
        "feature_importances": feature_importances,
        "permutation_importance": perm_importance_df,
        "shap_explainer": explainer,
        "shap_values_train": shap_values_train,
        "shap_values_test": shap_values_test,
        "train_preds": train_preds,
        "cv_preds": cv_preds,
        "test_preds": test_preds,
        "y_train": y_train,
        "y_test": y_test,
        "X_train": X_train,
        "X_test": X_test,
        "feature_cols": feature_cols
    }


def run_xgboost_pipeline():
    """
    Executes XGBoost tuning, training, and evaluation for both CSR and CRI.
    """
    train_df = pd.read_csv(config.PROCESSED_DATA_DIR / "train.csv")
    test_df = pd.read_csv(config.PROCESSED_DATA_DIR / "test.csv")

    csr_out = train_xgboost_model(train_df, test_df, target="CSR")
    cri_out = train_xgboost_model(train_df, test_df, target="CRI")

    # Export feature importances
    csr_fi_df = pd.DataFrame({
        "Gain_Importance": csr_out["feature_importances"],
        "Permutation_Importance": csr_out["permutation_importance"]["Permutation_Importance_Mean"]
    })
    csr_fi_df.to_csv(config.TABLES_DIR / "xgboost_csr_feature_importance.csv")

    cri_fi_df = pd.DataFrame({
        "Gain_Importance": cri_out["feature_importances"],
        "Permutation_Importance": cri_out["permutation_importance"]["Permutation_Importance_Mean"]
    })
    cri_fi_df.to_csv(config.TABLES_DIR / "xgboost_cri_feature_importance.csv")

    return {"CSR": csr_out, "CRI": cri_out}


if __name__ == "__main__":
    res = run_xgboost_pipeline()
    print("\n--- XGBoost CSR Results ---")
    print("Best Parameters:", res["CSR"]["best_params"])
    print(f"Train R2: {res['CSR']['train_metrics']['train_R2']:.4f}")
    print(f"CV R2: {res['CSR']['cv_metrics']['cv_mean_r2']:.4f} +/- {res['CSR']['cv_metrics']['cv_std_r2']:.4f}")
    print(f"CV RMSE: {res['CSR']['cv_metrics']['cv_mean_rmse']:.4f} +/- {res['CSR']['cv_metrics']['cv_std_rmse']:.4f}")
    print(f"Test R2: {res['CSR']['test_metrics']['test_R2']:.4f}, Test RMSE: {res['CSR']['test_metrics']['test_RMSE']:.4f}")

    print("\n--- XGBoost CRI Results ---")
    print("Best Parameters:", res["CRI"]["best_params"])
    print(f"Train R2: {res['CRI']['train_metrics']['train_R2']:.4f}")
    print(f"CV R2: {res['CRI']['cv_metrics']['cv_mean_r2']:.4f} +/- {res['CRI']['cv_metrics']['cv_std_r2']:.4f}")
    print(f"CV RMSE: {res['CRI']['cv_metrics']['cv_mean_rmse']:.4f} +/- {res['CRI']['cv_metrics']['cv_std_rmse']:.4f}")
    print(f"Test R2: {res['CRI']['test_metrics']['test_R2']:.4f}, Test RMSE: {res['CRI']['test_metrics']['test_RMSE']:.4f}")
