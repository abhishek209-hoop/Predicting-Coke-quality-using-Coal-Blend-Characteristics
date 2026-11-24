"""
Evaluation Module for Coke Quality Prediction Project.
Calculates research-grade regression metrics:
R2, Adjusted R2, RMSE, MAE, MSE, MAPE, Percentage MAE,
Median Absolute Error, Max Absolute Error, Explained Variance, and CV statistics.
"""

import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    median_absolute_error,
    max_error,
    explained_variance_score,
    mean_absolute_percentage_error
)

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config


def calculate_regression_metrics(y_true, y_pred, n_features=8, prefix=""):
    """
    Computes a comprehensive dictionary of regression evaluation metrics.
    
    Parameters:
    -----------
    y_true : array-like of shape (n_samples,)
        Ground truth actual values.
    y_pred : array-like of shape (n_samples,)
        Estimated target values.
    n_features : int, default=8
        Number of input predictors used for adjusted R2 calculation.
    prefix : str, default=""
        Prefix for metric keys (e.g., 'train_', 'test_').
        
    Returns:
    --------
    dict containing all computed metrics.
    """
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    n = len(y_true)

    # Core metrics
    r2 = r2_score(y_true, y_pred)
    
    # Adjusted R2
    if n > n_features + 1:
        adj_r2 = 1.0 - (1.0 - r2) * ((n - 1) / (n - n_features - 1))
    else:
        adj_r2 = np.nan

    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    med_ae = median_absolute_error(y_true, y_pred)
    max_ae = max_error(y_true, y_pred)
    evs = explained_variance_score(y_true, y_pred)
    
    # MAPE & Percentage MAE
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100.0  # as percentage
    mean_actual = np.mean(y_true)
    pct_mae = (mae / mean_actual) * 100.0 if mean_actual != 0 else np.nan

    metrics = {
        f"{prefix}R2": float(r2),
        f"{prefix}Adj_R2": float(adj_r2) if not np.isnan(adj_r2) else "N/A",
        f"{prefix}RMSE": float(rmse),
        f"{prefix}MAE": float(mae),
        f"{prefix}MSE": float(mse),
        f"{prefix}MAPE": float(mape),
        f"{prefix}Percentage_MAE": float(pct_mae),
        f"{prefix}Explained_Variance": float(evs),
        f"{prefix}Median_AE": float(med_ae),
        f"{prefix}Max_AE": float(max_ae)
    }
    return metrics


def format_metrics_table(metrics_list, model_names, target_name):
    """
    Formats a list of metrics dictionaries into a clean summary DataFrame.
    """
    df_metrics = pd.DataFrame(metrics_list, index=model_names)
    df_metrics.index.name = "Model"
    df_metrics.columns = [c.replace("_", " ") for c in df_metrics.columns]
    return df_metrics

