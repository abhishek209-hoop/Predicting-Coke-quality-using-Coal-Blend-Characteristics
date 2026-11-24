"""
Visualization Module for Coke Quality Prediction Project.
Generates publication-quality figures (300 DPI) for Exploratory Data Analysis,
Model Diagnostics (Actual vs Predicted, Residuals, QQ Plots), Feature Importances (Impurity, Permutation, SHAP),
Decision Tree structures, and comprehensive Model Comparative Evaluations.
"""

import sys
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
# pyrefly: ignore[missing-import]
from scipy import stats
from sklearn.tree import plot_tree
# pyrefly: ignore[missing-import]
import shap

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

# Set global matplotlib scientific styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})


def plot_distributions_and_boxplots(df, feature_cols=None, target_cols=None, save_dir=config.GRAPHS_DIR):
    """
    Plots individual histograms with KDE and boxplots for all 8 features and 2 targets.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
    if target_cols is None:
        target_cols = config.TARGET_COLUMNS

    all_cols = feature_cols + target_cols

    # 1. Multi-panel Histogram + KDE Grid
    fig, axes = plt.subplots(3, 4, figsize=(16, 11))
    axes = axes.flatten()

    for i, col in enumerate(all_cols):
        ax = axes[i]
        sns.histplot(df[col], kde=True, ax=ax, color="#1f77b4", edgecolor="black", alpha=0.6)
        unit = config.FEATURE_METADATA.get(col, {}).get("unit", "")
        ax.set_title(f"{col} Distribution", fontweight="bold")
        ax.set_xlabel(f"{col} ({unit})")
        ax.set_ylabel("Frequency")
        ax.grid(True, linestyle="--", alpha=0.5)

    # Hide unused subplots
    for j in range(len(all_cols), len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle("Distributions and Density Profiles of Coal Properties and Coke Targets", y=1.02, fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "eda_histograms_kde.png")
    plt.close()

    # 2. Multi-panel Boxplots
    fig, axes = plt.subplots(3, 4, figsize=(16, 11))
    axes = axes.flatten()

    for i, col in enumerate(all_cols):
        ax = axes[i]
        sns.boxplot(y=df[col], ax=ax, color="#aec7e8", width=0.4, flierprops=dict(marker="o", markerfacecolor="red", markersize=6))
        unit = config.FEATURE_METADATA.get(col, {}).get("unit", "")
        ax.set_title(f"{col} Boxplot", fontweight="bold")
        ax.set_ylabel(f"{col} ({unit})")
        ax.grid(True, linestyle="--", alpha=0.5)

    for j in range(len(all_cols), len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle("Univariate Boxplot Profiles Identifying Dispersion and Potential Outliers", y=1.02, fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "eda_boxplots.png")
    plt.close()


def plot_correlation_heatmaps(corr_dict, save_dir=config.GRAPHS_DIR):
    """
    Plots correlation heatmaps:
    - Feature vs Target correlation heatmap (Pearson and Spearman side-by-side)
    - Full Pearson correlation matrix heatmap
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # 1. Feature vs Target Heatmap
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    sns.heatmap(
        corr_dict["pearson_feat_target"],
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        cbar=True,
        ax=axes[0],
        linewidths=0.5
    )
    axes[0].set_title("Pearson Correlation with Targets", fontweight="bold")
    axes[0].set_ylabel("Coal Characteristics")

    sns.heatmap(
        corr_dict["spearman_feat_target"],
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        cbar=True,
        ax=axes[1],
        linewidths=0.5
    )
    axes[1].set_title("Spearman Rank Correlation with Targets", fontweight="bold")
    axes[1].set_ylabel("")

    plt.suptitle("Coal Blend Characteristics vs Coke CSR and CRI Targets", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "eda_feature_target_correlation.png")
    plt.close()

    # 2. Full Feature Inter-Correlation Matrix
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_dict["pearson_feat_feat"], dtype=bool), k=1)
    sns.heatmap(
        corr_dict["pearson_feat_feat"],
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Inter-Feature Pearson Correlation Matrix (Highlighting TR-TI Collinearity)", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(save_dir / "eda_feature_intercorrelation_matrix.png")
    plt.close()


def plot_feature_target_scatterplots(df, feature_cols=None, save_dir=config.GRAPHS_DIR):
    """
    Plots individual scatter plots for each of the 8 features against CSR and CRI with regression trend lines.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    if feature_cols is None:
        feature_cols = config.STANDARDIZED_FEATURE_COLUMNS

    for target in config.TARGET_COLUMNS:
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.flatten()

        for i, col in enumerate(feature_cols):
            ax = axes[i]
            sns.regplot(
                data=df,
                x=col,
                y=target,
                ax=ax,
                color="#2ca02c" if target == "CSR" else "#d62728",
                scatter_kws={"alpha": 0.7, "edgecolor": "k", "s": 40},
                line_kws={"color": "black", "linewidth": 1.5}
            )
            unit_x = config.FEATURE_METADATA.get(col, {}).get("unit", "")
            unit_y = config.FEATURE_METADATA.get(target, {}).get("unit", "")
            r_val = df[col].corr(df[target])
            ax.set_title(f"{col} vs {target} (r = {r_val:.2f})", fontweight="bold")
            ax.set_xlabel(f"{col} ({unit_x})")
            ax.set_ylabel(f"{target} ({unit_y})")
            ax.grid(True, linestyle="--", alpha=0.5)

        plt.suptitle(f"Bivariate Scatter Profiles with Linear Fits: Coal Properties vs Coke {target}", y=1.02, fontsize=15, fontweight="bold")
        plt.tight_layout()
        plt.savefig(save_dir / f"eda_scatter_{target.lower()}.png")
        plt.close()


def plot_vif_chart(vif_df, save_dir=config.GRAPHS_DIR):
    """
    Generates bar chart showing VIF across all 8 features, contrasting with and without TI.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    features = vif_df.index
    vif_vals = vif_df["VIF_with_constant"]

    bars = plt.bar(features, vif_vals, color="#e377c2", edgecolor="black")
    plt.axhline(y=10, color="red", linestyle="--", linewidth=1.5, label="Severe Multicollinearity Threshold (VIF=10)")
    plt.axhline(y=5, color="orange", linestyle=":", linewidth=1.5, label="Moderate Collinearity Threshold (VIF=5)")
    plt.yscale("log")
    plt.title("Variance Inflation Factor (VIF) Across 8 Coal Predictors (Log Scale)", fontsize=13, fontweight="bold")
    plt.xlabel("Predictor Variable")
    plt.ylabel("VIF (Log Scale)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    for bar, val in zip(bars, vif_vals):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval * 1.2, f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_dir / "eda_vif_barchart.png")
    plt.close()


def plot_actual_vs_predicted(y_train, train_preds, y_test, test_preds, model_name, target, save_dir=config.GRAPHS_DIR):
    """
    Generates actual versus predicted scatter plot distinguishing training and test observations,
    with 45-degree line and performance annotations.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 7))

    # Scatter points
    plt.scatter(y_train, train_preds, color="#1f77b4", alpha=0.6, edgecolors="none", s=50, label="Train Set (n=54)")
    plt.scatter(y_test, test_preds, color="#ff7f0e", alpha=0.9, edgecolors="black", s=80, marker="^", label="Test Set (n=14)")

    # 45-degree reference line
    all_vals = np.concatenate([y_train, train_preds, y_test, test_preds])
    min_val = np.min(all_vals) - 2
    max_val = np.max(all_vals) + 2
    plt.plot([min_val, max_val], [min_val, max_val], "k--", linewidth=1.5, label="Ideal 1:1 Line")

    # Annotate metrics
    from sklearn.metrics import r2_score, root_mean_squared_error
    train_r2 = r2_score(y_train, train_preds)
    test_r2 = r2_score(y_test, test_preds)
    test_rmse = root_mean_squared_error(y_test, test_preds)

    unit = config.FEATURE_METADATA.get(target, {}).get("unit", "")
    plt.title(f"{model_name}: Actual vs Predicted {target}", fontsize=13, fontweight="bold")
    plt.xlabel(f"Actual {target} ({unit})")
    plt.ylabel(f"Predicted {target} ({unit})")
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)

    stats_text = f"Train $R^2$: {train_r2:.3f}\nTest $R^2$: {test_r2:.3f}\nTest RMSE: {test_rmse:.2f} {unit}"
    plt.text(0.05, 0.85, stats_text, transform=plt.gca().transAxes, fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8, edgecolor="gray"))

    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    filename = f"{model_name.lower().replace(' ', '_')}_{target.lower()}_act_vs_pred.png"
    plt.savefig(save_dir / filename)
    plt.close()


def plot_residual_diagnostics(y_train, train_preds, y_test, test_preds, model_name, target, save_dir=config.GRAPHS_DIR):
    """
    Creates a 4-panel residual diagnostic graph:
    1. Residuals vs Predicted
    2. Residuals vs Actual
    3. Residual Histogram with KDE
    4. Normal Q-Q Plot
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    residuals_train = y_train - train_preds
    residuals_test = y_test - test_preds
    unit = config.FEATURE_METADATA.get(target, {}).get("unit", "")

    fig, axes = plt.subplots(2, 2, figsize=(13, 11))

    # 1. Residuals vs Predicted
    ax1 = axes[0, 0]
    ax1.scatter(train_preds, residuals_train, color="#1f77b4", alpha=0.6, label="Train")
    ax1.scatter(test_preds, residuals_test, color="#ff7f0e", edgecolors="k", marker="^", s=70, label="Test")
    ax1.axhline(0, color="red", linestyle="--", linewidth=1.5)
    ax1.set_title(f"Residuals vs Predicted {target}", fontweight="bold")
    ax1.set_xlabel(f"Predicted {target} ({unit})")
    ax1.set_ylabel(f"Residuals ({unit})")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 2. Residuals vs Actual
    ax2 = axes[0, 1]
    ax2.scatter(y_train, residuals_train, color="#1f77b4", alpha=0.6, label="Train")
    ax2.scatter(y_test, residuals_test, color="#ff7f0e", edgecolors="k", marker="^", s=70, label="Test")
    ax2.axhline(0, color="red", linestyle="--", linewidth=1.5)
    ax2.set_title(f"Residuals vs Actual {target}", fontweight="bold")
    ax2.set_xlabel(f"Actual {target} ({unit})")
    ax2.set_ylabel(f"Residuals ({unit})")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.5)

    # 3. Residual Distribution Histogram + KDE
    ax3 = axes[1, 0]
    sns.histplot(residuals_train, kde=True, ax=ax3, color="#1f77b4", label="Train Residuals", alpha=0.5)
    sns.histplot(residuals_test, kde=True, ax=ax3, color="#ff7f0e", label="Test Residuals", alpha=0.6)
    ax3.set_title(f"Residual Error Distribution ({target})", fontweight="bold")
    ax3.set_xlabel(f"Residual Error ({unit})")
    ax3.set_ylabel("Frequency")
    ax3.legend()
    ax3.grid(True, linestyle="--", alpha=0.5)

    # 4. Normal Q-Q Plot
    ax4 = axes[1, 1]
    stats.probplot(residuals_train, dist="norm", plot=ax4)
    ax4.get_lines()[0].set_color("#1f77b4")
    ax4.get_lines()[0].set_label("Train Quantiles")
    ax4.get_lines()[1].set_color("red")
    ax4.set_title(f"Normal Q-Q Plot of Residuals ({target})", fontweight="bold")
    ax4.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle(f"{model_name} Residual Diagnostic Suite for Coke {target}", y=1.02, fontsize=15, fontweight="bold")
    plt.tight_layout()
    filename = f"{model_name.lower().replace(' ', '_')}_{target.lower()}_residuals.png"
    plt.savefig(save_dir / filename)
    plt.close()


def plot_feature_importance_comparison(fi_series, title, xlabel, save_path, color="#2b5c8f"):
    """
    Plots horizontal bar chart of feature importances.
    """
    plt.figure(figsize=(8, 5))
    sorted_fi = fi_series.sort_values(ascending=True)
    plt.barh(sorted_fi.index, sorted_fi.values, color=color, edgecolor="black")
    plt.title(title, fontsize=12, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel("Predictor Variable")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_tree_structure(decision_tree_model, feature_names, target, save_path):
    """
    Plots readable visual diagram of fitted Decision Tree.
    """
    plt.figure(figsize=(14, 8))
    plot_tree(
        decision_tree_model,
        feature_names=feature_names,
        filled=True,
        rounded=True,
        precision=2,
        fontsize=9
    )
    plt.title(f"Optimized Pruned Decision Tree Architecture for {target} Prediction", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_shap_summary(explainer, shap_values, X, feature_names, target, save_path):
    """
    Generates SHAP summary plot (beeswarm).
    """
    plt.figure(figsize=(9, 6))
    shap.summary_plot(shap_values, X, feature_names=feature_names, show=False)
    plt.title(f"SHAP Feature Importance & Attribution for {target} (XGBoost)", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_model_comparisons(comparison_df_csr, comparison_df_cri, save_dir=config.GRAPHS_DIR):
    """
    Creates comparative bar charts across all 4 models:
    - Test R2 Comparison (CSR and CRI)
    - Test RMSE Comparison (CSR and CRI)
    - Test MAE Comparison (CSR and CRI)
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    models = comparison_df_csr.index.tolist()
    colors = ["#4c72b0", "#55a868", "#c44e52", "#8172b3"]

    # 1. Test R2 Comparison
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].bar(models, comparison_df_csr["test_R2"], color=colors, edgecolor="black")
    axes[0].axhline(0, color="k", linestyle="--", linewidth=1)
    axes[0].set_title("CSR: Test $R^2$ Comparison", fontweight="bold")
    axes[0].set_ylabel("Test $R^2$ Score")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    axes[1].bar(models, comparison_df_cri["test_R2"], color=colors, edgecolor="black")
    axes[1].axhline(0, color="k", linestyle="--", linewidth=1)
    axes[1].set_title("CRI: Test $R^2$ Comparison", fontweight="bold")
    axes[1].set_ylabel("Test $R^2$ Score")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Model Generalization Comparison: Test $R^2$ Across Four Algorithms", y=1.02, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "comparison_test_r2.png")
    plt.close()

    # 2. Test RMSE Comparison
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].bar(models, comparison_df_csr["test_RMSE"], color=colors, edgecolor="black")
    axes[0].set_title("CSR: Test RMSE Comparison (Lower is Better)", fontweight="bold")
    axes[0].set_ylabel("Test RMSE (%)")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    axes[1].bar(models, comparison_df_cri["test_RMSE"], color=colors, edgecolor="black")
    axes[1].set_title("CRI: Test RMSE Comparison (Lower is Better)", fontweight="bold")
    axes[1].set_ylabel("Test RMSE (%)")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Model Predictive Accuracy: Test RMSE Across Four Algorithms", y=1.02, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "comparison_test_rmse.png")
    plt.close()

    # 3. Test MAE Comparison
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].bar(models, comparison_df_csr["test_MAE"], color=colors, edgecolor="black")
    axes[0].set_title("CSR: Test MAE Comparison", fontweight="bold")
    axes[0].set_ylabel("Test MAE (%)")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    axes[1].bar(models, comparison_df_cri["test_MAE"], color=colors, edgecolor="black")
    axes[1].set_title("CRI: Test MAE Comparison", fontweight="bold")
    axes[1].set_ylabel("Test MAE (%)")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Model Absolute Error: Test MAE Across Four Algorithms", y=1.02, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / "comparison_test_mae.png")
    plt.close()

