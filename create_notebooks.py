"""
Script to create the 9 required Jupyter notebooks in the notebooks/ folder.
"""

from pathlib import Path
# pyrefly: ignore[missing-import]
import nbformat as nbf

nb_dir = Path("notebooks")
nb_dir.mkdir(exist_ok=True)

notebook_specs = [
    ("01_Data_Inspection.ipynb", [
        ("markdown", "# Phase 1: Data Ingestion & Initial Inspection\nThis notebook inspects the raw coal-blend and coke quality dataset inspired by Dash et al. (2012)."),
        ("code", """import pandas as pd
import numpy as np

# Load raw CSV
df_raw = pd.read_csv('../data/raw/coal_coke_data.csv', header=1)
df_raw.index.name = 'Serial_No'
df_raw = df_raw.reset_index()

print("Shape:", df_raw.shape)
print("Columns:", df_raw.columns.tolist())
display(df_raw.head(10))
print(df_raw.info())
"""),
        ("markdown", "### Column Mapping and Data Types\nVerify data types and map raw headers to standardized metallurgical naming conventions.")
    ]),
    ("02_Data_Cleaning.ipynb", [
        ("markdown", "# Phase 2: Data Cleaning & Preprocessing Audit\nThis notebook audits missing values, duplicates, out-of-range values, and checks the compositional closure constraint (Total Reactives + Total Inerts = 100)."),
        ("code", """import sys
from pathlib import Path
sys.path.append('..')
import config
from src.data_preprocessing import load_raw_data, audit_data_quality, preprocess_and_split

df = load_raw_data()
audit = audit_data_quality(df)

print("Missing Values:")
display(audit['missing_values'])

print("TR + TI Sum Statistics:")
print(audit['tr_ti_sum_stats'])

print("Notable Anomalous Observations:")
display(audit['notable_observations'])

split_dict = preprocess_and_split(df)
print(f"Train size: {len(split_dict['train_df'])}, Test size: {len(split_dict['test_df'])}")
""")
    ]),
    ("03_Exploratory_Data_Analysis.ipynb", [
        ("markdown", "# Phase 3: Exploratory Data Analysis & Statistical Profiling\nDescriptive profiling, Pearson & Spearman correlations, and bivariate relationships between 8 coal properties and CSR / CRI targets."),
        ("code", """import sys
sys.path.append('..')
import pandas as pd
import config
from src.eda import run_eda_pipeline

df = pd.read_csv('../data/processed/cleaned_coal_coke.csv')
eda_res = run_eda_pipeline(df)

print("Descriptive Statistics Table:")
display(eda_res['stats_df'])

print("Pearson Feature-Target Correlations:")
display(eda_res['corr_dict']['pearson_feat_target'])

print("Multicollinearity Diagnostics (VIF Table):")
display(eda_res['vif_table'])
""")
    ]),
    ("04_MLR_Phase1.ipynb", [
        ("markdown", "# Phase 4: Multiple Linear Regression (MLR) - Phase 1 Baseline\nFits full 8-variable OLS regression models for CSR and CRI as in Dash et al. (2012) Phase 1."),
        ("code", """import sys
sys.path.append('..')
from src.mlr_model import run_mlr_phase1

res = run_mlr_phase1()

print("=== CSR MLR Regression Equation ===")
print(res['CSR']['equation_str'])
display(res['CSR']['coef_df'])

print("=== CRI MLR Regression Equation ===")
print(res['CRI']['equation_str'])
display(res['CRI']['coef_df'])
""")
    ]),
    ("05_XGBoost.ipynb", [
        ("markdown", "# Phase 5: XGBoost Regressor Model\nOptimizes gradient boosted regression trees for CSR and CRI using 5-fold cross-validation."),
        ("code", """import sys
sys.path.append('..')
from src.xgboost_model import run_xgboost_pipeline

res = run_xgboost_pipeline()

print("Best CSR Parameters:", res['CSR']['best_params'])
print(f"CSR Test RMSE: {res['CSR']['test_metrics']['test_RMSE']:.4f}, Test R2: {res['CSR']['test_metrics']['test_R2']:.4f}")

print("Best CRI Parameters:", res['CRI']['best_params'])
print(f"CRI Test RMSE: {res['CRI']['test_metrics']['test_RMSE']:.4f}, Test R2: {res['CRI']['test_metrics']['test_R2']:.4f}")
""")
    ]),
    ("06_Random_Forest.ipynb", [
        ("markdown", "# Phase 6: Random Forest Regressor Model\nOptimizes ensemble of bagged decision trees using 5-fold cross-validation."),
        ("code", """import sys
sys.path.append('..')
from src.random_forest_model import run_random_forest_pipeline

res = run_random_forest_pipeline()

print("Best CSR Parameters:", res['CSR']['best_params'])
print(f"CSR Test RMSE: {res['CSR']['test_metrics']['test_RMSE']:.4f}, Test R2: {res['CSR']['test_metrics']['test_R2']:.4f}")

print("Best CRI Parameters:", res['CRI']['best_params'])
print(f"CRI Test RMSE: {res['CRI']['test_metrics']['test_RMSE']:.4f}, Test R2: {res['CRI']['test_metrics']['test_R2']:.4f}")
""")
    ]),
    ("07_Decision_Tree.ipynb", [
        ("markdown", "# Phase 7: Decision Tree Regressor with Cost-Complexity Pruning\nOptimizes interpretable single decision trees, extracts decision rules, and evaluates generalization."),
        ("code", """import sys
sys.path.append('..')
from src.decision_tree_model import run_decision_tree_pipeline

res = run_decision_tree_pipeline()

print("=== CSR Decision Tree Rules ===")
print(res['CSR']['tree_rules_text'])

print("=== CRI Decision Tree Rules ===")
print(res['CRI']['tree_rules_text'])
""")
    ]),
    ("08_Model_Comparison.ipynb", [
        ("markdown", "# Phase 8: Cross-Model Comparative Synthesis\nCompares all 4 models across R2, RMSE, MAE, MSE, MAPE, Explained Variance, and CV metrics for CSR and CRI separately."),
        ("code", """import pandas as pd

csr_comp = pd.read_csv('../results/tables/csr_model_comparison.csv', index_col=0)
cri_comp = pd.read_csv('../results/tables/cri_model_comparison.csv', index_col=0)

print("=== CSR MODEL COMPARATIVE SUMMARY ===")
display(csr_comp)

print("=== CRI MODEL COMPARATIVE SUMMARY ===")
display(cri_comp)
""")
    ]),
    ("09_Explainability.ipynb", [
        ("markdown", "# Phase 9: Model Explainability & SHAP Attribution\nAnalyzes feature importances across algorithms (MDI, Permutation, OLS beta coefficients) and SHAP values."),
        ("code", """import pandas as pd
import matplotlib.pyplot as plt

xgb_csr_fi = pd.read_csv('../results/tables/xgboost_csr_feature_importance.csv', index_col=0)
rf_csr_fi = pd.read_csv('../results/tables/rf_csr_feature_importance.csv', index_col=0)

print("XGBoost Feature Importance (Gain & Permutation):")
display(xgb_csr_fi)

print("Random Forest Feature Importance (MDI & Permutation):")
display(rf_csr_fi)
""")
    ])
]

for filename, cells in notebook_specs:
    nb = nbf.v4.new_notebook()
    nb_cells = []
    for ctype, content in cells:
        if ctype == "markdown":
            nb_cells.append(nbf.v4.new_markdown_cell(content))
        elif ctype == "code":
            nb_cells.append(nbf.v4.new_code_cell(content))
    nb["cells"] = nb_cells
    nb_path = nb_dir / filename
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Created {filename}")

