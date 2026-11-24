"""
Master Orchestration Script for Coke Quality Prediction Project.
Executes the complete end-to-end scientific machine learning pipeline:
Data Ingestion -> Cleaning & Splitting -> EDA -> Multicollinearity Diagnostics ->
4 Regression Models (MLR, XGBoost, Random Forest, Decision Tree) for CSR and CRI ->
Model Evaluation & Diagnostics -> Publication Figures -> Comparative Tabular Reports.
"""

import sys
import time
from pathlib import Path
import pandas as pd
# pyrefly: ignore[missing-import]
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
import config
from src.data_preprocessing import load_raw_data, audit_data_quality, preprocess_and_split
from src.eda import run_eda_pipeline
from src.mlr_model import run_mlr_phase1
from src.xgboost_model import run_xgboost_pipeline
from src.random_forest_model import run_random_forest_pipeline
from src.decision_tree_model import run_decision_tree_pipeline
from src.visualization import (
    plot_distributions_and_boxplots,
    plot_correlation_heatmaps,
    plot_feature_target_scatterplots,
    plot_vif_chart,
    plot_actual_vs_predicted,
    plot_residual_diagnostics,
    plot_feature_importance_comparison,
    plot_tree_structure,
    plot_shap_summary,
    plot_model_comparisons
)
from src.prediction import CokeQualityPredictor


def main():
    start_time = time.time()
    print("=" * 80)
    print("COKE QUALITY PREDICTION RESEARCH PROJECT: END-TO-END PIPELINE")
    print("Scientific Reference: Dash et al. (2012) Comparative Reproduction & ML Evaluation")
    print("=" * 80)

    # -------------------------------------------------------------
    # PHASE 1 & 2: DATA INGESTION, AUDIT, AND PREPROCESSING
    # -------------------------------------------------------------
    print("\n>>> PHASE 1 & 2: Ingesting Raw Data and Performing Quality Audit...")
    df_raw = load_raw_data()
    audit_report = audit_data_quality(df_raw)
    print(f"Loaded {audit_report['n_rows']} observations across {audit_report['n_cols']} columns.")
    print(f"Missing Values: {audit_report['missing_values']['Missing_Count'].sum()} | Exact Duplicates: {audit_report['exact_duplicates_count']}")
    print(f"Compositional TR+TI Mean: {audit_report['tr_ti_sum_stats']['mean']:.4f} (Max Dev: {audit_report['tr_ti_sum_stats']['max_deviation_from_100']:.4f}%)")

    # Splitting
    split_res = preprocess_and_split(df_raw)
    train_df = split_res["train_df"]
    test_df = split_res["test_df"]
    clean_df = split_res["full_df"]
    print(f"Dataset split: Train = {len(train_df)} observations (80%), Test = {len(test_df)} observations (20%).")

    # -------------------------------------------------------------
    # PHASE 3 & 4: EXPLORATORY DATA ANALYSIS & MULTICOLLINEARITY
    # -------------------------------------------------------------
    print("\n>>> PHASE 3 & 4: Running Exploratory Data Analysis & Collinearity Diagnostics...")
    eda_res = run_eda_pipeline(clean_df)
    vif_table = eda_res["vif_table"]
    print("Multicollinearity Diagnostics:")
    print(vif_table[["VIF_with_constant", "VIF_without_TI"]])

    # Generate EDA figures
    print("Generating publication-grade EDA visualizations...")
    plot_distributions_and_boxplots(clean_df)
    plot_correlation_heatmaps(eda_res["corr_dict"])
    plot_feature_target_scatterplots(clean_df)
    plot_vif_chart(vif_table)

    # -------------------------------------------------------------
    # PHASE 5, 6 & 7: MODEL TRAINING & EVALUATION (CSR & CRI)
    # -------------------------------------------------------------
    print("\n>>> PHASE 5, 6 & 7: Training and Evaluating Four ML Algorithms...")

    # 1. Multiple Linear Regression Phase 1
    print("\n[1/4] Fitting Model 1: Multiple Linear Regression (Phase 1 Baseline)...")
    mlr_res = run_mlr_phase1()

    # 2. XGBoost Regressor
    print("\n[2/4] Optimizing Model 2: XGBoost Regressor via 5-Fold Cross-Validation...")
    xgb_res = run_xgboost_pipeline()

    # 3. Random Forest Regressor
    print("\n[3/4] Optimizing Model 3: Random Forest Regressor via 5-Fold Cross-Validation...")
    rf_res = run_random_forest_pipeline()

    # 4. Decision Tree Regressor
    print("\n[4/4] Optimizing Model 4: Decision Tree Regressor with Cost-Complexity Pruning...")
    dt_res = run_decision_tree_pipeline()

    # -------------------------------------------------------------
    # PHASE 8: DIAGNOSTIC PLOTS FOR ALL MODELS
    # -------------------------------------------------------------
    print("\n>>> Generating Diagnostic Figures (Actual vs Predicted & Residual Suites)...")
    models_dict = {
        "MLR Phase 1": mlr_res,
        "XGBoost": xgb_res,
        "Random Forest": rf_res,
        "Decision Tree": dt_res
    }

    for model_name, m_dict in models_dict.items():
        for target in ["CSR", "CRI"]:
            res_obj = m_dict[target]
            # Actual vs Predicted
            plot_actual_vs_predicted(
                res_obj["y_train"], res_obj["train_preds"],
                res_obj["y_test"], res_obj["test_preds"],
                model_name=model_name, target=target
            )
            # Residual Suite
            plot_residual_diagnostics(
                res_obj["y_train"], res_obj["train_preds"],
                res_obj["y_test"], res_obj["test_preds"],
                model_name=model_name, target=target
            )

    # Decision Tree Structural Diagrams
    print("Rendering pruned Decision Tree graphical structures...")
    plot_tree_structure(
        dt_res["CSR"]["best_model"],
        feature_names=config.STANDARDIZED_FEATURE_COLUMNS,
        target="CSR",
        save_path=config.GRAPHS_DIR / "decision_tree_csr_structure.png"
    )
    plot_tree_structure(
        dt_res["CRI"]["best_model"],
        feature_names=config.STANDARDIZED_FEATURE_COLUMNS,
        target="CRI",
        save_path=config.GRAPHS_DIR / "decision_tree_cri_structure.png"
    )

    # SHAP Explanations for XGBoost
    print("Generating SHAP summary attributions for XGBoost...")
    plot_shap_summary(
        xgb_res["CSR"]["shap_explainer"],
        xgb_res["CSR"]["shap_values_train"],
        xgb_res["CSR"]["X_train"],
        feature_names=config.STANDARDIZED_FEATURE_COLUMNS,
        target="CSR",
        save_path=config.GRAPHS_DIR / "xgboost_csr_shap_summary.png"
    )
    plot_shap_summary(
        xgb_res["CRI"]["shap_explainer"],
        xgb_res["CRI"]["shap_values_train"],
        xgb_res["CRI"]["X_train"],
        feature_names=config.STANDARDIZED_FEATURE_COLUMNS,
        target="CRI",
        save_path=config.GRAPHS_DIR / "xgboost_cri_shap_summary.png"
    )

    # -------------------------------------------------------------
    # PHASE 9 & 10: COMPARATIVE PERFORMANCE MATRICES & SYNTHESIS
    # -------------------------------------------------------------
    print("\n>>> Building Comprehensive Comparative Evaluation Tables...")
    
    def compile_target_comparison(target_name):
        rows = []
        for model_name, m_dict in models_dict.items():
            r = m_dict[target_name]
            test_m = r["test_metrics"]
            cv_m = r["cv_metrics"]
            train_m = r["train_metrics"]
            
            row = {
                "Model": model_name,
                "Train_R2": train_m[f"train_R2"],
                "Test_R2": test_m[f"test_R2"],
                "Test_Adj_R2": test_m[f"test_Adj_R2"] if model_name == "MLR Phase 1" else "N/A",
                "Test_RMSE": test_m[f"test_RMSE"],
                "Test_MAE": test_m[f"test_MAE"],
                "Test_MSE": test_m[f"test_MSE"],
                "Test_MAPE (%)": test_m[f"test_MAPE"],
                "Percentage_MAE (%)": test_m[f"test_Percentage_MAE"],
                "Explained_Variance": test_m[f"test_Explained_Variance"],
                "Median_AE": test_m[f"test_Median_AE"],
                "Max_AE": test_m[f"test_Max_AE"],
                "CV_R2_Mean": cv_m["cv_mean_r2"],
                "CV_R2_Std": cv_m["cv_std_r2"],
                "CV_RMSE_Mean": cv_m["cv_mean_rmse"],
                "CV_RMSE_Std": cv_m["cv_std_rmse"]
            }
            rows.append(row)
        df_comp = pd.DataFrame(rows).set_index("Model")
        return df_comp

    csr_comparison = compile_target_comparison("CSR")
    cri_comparison = compile_target_comparison("CRI")

    # Export comparison tables to CSV and Excel
    csr_comparison.to_csv(config.TABLES_DIR / "csr_model_comparison.csv")
    csr_comparison.to_excel(config.TABLES_DIR / "csr_model_comparison.xlsx")

    cri_comparison.to_csv(config.TABLES_DIR / "cri_model_comparison.csv")
    cri_comparison.to_excel(config.TABLES_DIR / "cri_model_comparison.xlsx")

    with pd.ExcelWriter(config.TABLES_DIR / "master_model_comparison.xlsx") as writer:
        csr_comparison.to_excel(writer, sheet_name="CSR_Comparison")
        cri_comparison.to_excel(writer, sheet_name="CRI_Comparison")

    # Comparative graphs
    plot_model_comparisons(
        csr_comparison.rename(columns={"Test_R2": "test_R2", "Test_RMSE": "test_RMSE", "Test_MAE": "test_MAE"}),
        cri_comparison.rename(columns={"Test_R2": "test_R2", "Test_RMSE": "test_RMSE", "Test_MAE": "test_MAE"})
    )

    print("\n" + "=" * 50)
    print("FINAL CSR MODEL COMPARISON")
    print("=" * 50)
    print(csr_comparison[["Test_R2", "Test_RMSE", "Test_MAE", "CV_R2_Mean", "CV_RMSE_Mean"]])

    print("\n" + "=" * 50)
    print("FINAL CRI MODEL COMPARISON")
    print("=" * 50)
    print(cri_comparison[["Test_R2", "Test_RMSE", "Test_MAE", "CV_R2_Mean", "CV_RMSE_Mean"]])

    # -------------------------------------------------------------
    # VERIFY INFERENCE PIPELINE
    # -------------------------------------------------------------
    print("\n>>> Testing Standalone Inference Engine (prediction.py)...")
    predictor = CokeQualityPredictor(csr_model_type="xgboost", cri_model_type="random_forest")
    sample_test = test_df.iloc[0][config.STANDARDIZED_FEATURE_COLUMNS].to_dict()
    pred_res = predictor.predict(sample_test)
    print("Sample Blend Predictor Check:")
    print("Actual Values  -> CSR:", test_df.iloc[0]["CSR"], "% | CRI:", test_df.iloc[0]["CRI"], "%")
    print("Predicted Values -> CSR:", pred_res["predictions"]["Predicted_CSR (%)"].iloc[0], "% | CRI:", pred_res["predictions"]["Predicted_CRI (%)"].iloc[0], "%")

    elapsed = time.time() - start_time
    print(f"\nPipeline successfully completed in {elapsed:.2f} seconds.")
    print("All models, tables, figures, and predictions successfully saved.")


if __name__ == "__main__":
    main()

