"""
Configuration settings for Coke Quality Prediction Project.
Defines directory paths, feature mappings, target variables, random seeds,
and hyperparameter search grids for reproducible ML pipelines.
"""

from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "coal_coke_data.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = BASE_DIR / "models"
MODELS_CSR_DIR = MODELS_DIR / "csr"
MODELS_CRI_DIR = MODELS_DIR / "cri"

RESULTS_DIR = BASE_DIR / "results"
TABLES_DIR = RESULTS_DIR / "tables"
GRAPHS_DIR = RESULTS_DIR / "graphs"
METRICS_DIR = RESULTS_DIR / "metrics"
PREDICTIONS_DIR = RESULTS_DIR / "predictions"

REPORTS_DIR = BASE_DIR / "reports"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Reproducibility settings
RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

# Column Names & Mappings
RAW_FEATURE_COLUMNS = [
    "Ash",
    "VM",
    "Ro",
    "V9–V13",
    "Total reactive",
    "Total inert",
    "CSN",
    "BI"
]

STANDARDIZED_FEATURE_COLUMNS = [
    "Ash",
    "VM",
    "Ro",
    "V9_V13",
    "TR",
    "TI",
    "CSN",
    "BI"
]

COLUMN_MAPPING = {
    "Ash": "Ash",
    "VM": "VM",
    "Ro": "Ro",
    "V9–V13": "V9_V13",
    "V9-V13": "V9_V13",
    "Total reactive": "TR",
    "Total inert": "TI",
    "CSN": "CSN",
    "BI": "BI",
    "CSR": "CSR",
    "CRI": "CRI"
}

TARGET_COLUMNS = ["CSR", "CRI"]

# Metallurgical plausible ranges and units
FEATURE_METADATA = {
    "Ash": {"unit": "%", "full_name": "Coal Blend Ash Content", "min": 5.0, "max": 25.0},
    "VM": {"unit": "%", "full_name": "Volatile Matter", "min": 15.0, "max": 35.0},
    "Ro": {"unit": "%", "full_name": "Mean Vitrinite Reflectance", "min": 0.8, "max": 1.6},
    "V9_V13": {"unit": "%", "full_name": "Vitrinite Distribution (V9-V13)", "min": 30.0, "max": 100.0},
    "TR": {"unit": "%", "full_name": "Total Reactives", "min": 30.0, "max": 70.0},
    "TI": {"unit": "%", "full_name": "Total Inerts", "min": 30.0, "max": 70.0},
    "CSN": {"unit": "Index", "full_name": "Crucible Swelling Number", "min": 1.0, "max": 9.0},
    "BI": {"unit": "Ratio", "full_name": "Basicity Index", "min": 0.02, "max": 0.35},
    "CSR": {"unit": "%", "full_name": "Coke Strength after Reaction", "min": 10.0, "max": 80.0},
    "CRI": {"unit": "%", "full_name": "Coke Reactivity Index", "min": 15.0, "max": 60.0}
}

# Hyperparameter Search Spaces (Carefully bounded for small n=54 training samples)
DECISION_TREE_PARAM_GRID = {
    "max_depth": [2, 3, 4, 5, None],
    "min_samples_split": [2, 4, 6],
    "min_samples_leaf": [1, 2, 4],
    "max_features": [None, "sqrt", "log2", 0.8],
    "ccp_alpha": [0.0, 0.05, 0.1, 0.2]
}

RANDOM_FOREST_PARAM_GRID = {
    "n_estimators": [30, 50, 100],
    "max_depth": [3, 4, 5, 6, None],
    "min_samples_split": [2, 4],
    "min_samples_leaf": [1, 2, 3],
    "max_features": ["sqrt", "log2", 0.7, 1.0],
    "bootstrap": [True]
}

XGBOOST_PARAM_GRID = {
    "n_estimators": [30, 50, 80, 100],
    "max_depth": [2, 3, 4],
    "learning_rate": [0.03, 0.05, 0.08, 0.1, 0.15],
    "subsample": [0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.7, 0.8, 1.0],
    "min_child_weight": [1, 2, 3],
    "gamma": [0.0, 0.05, 0.1],
    "reg_alpha": [0.0, 0.1, 1.0],
    "reg_lambda": [0.5, 1.0, 2.0]
}
