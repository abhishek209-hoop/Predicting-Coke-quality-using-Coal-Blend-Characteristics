# Coke Quality Prediction: Machine Learning Comparative Evaluation

An end-to-end, research-grade machine learning project investigating the prediction of Coke Strength after Reaction (**CSR**) and Coke Reactivity Index (**CRI**) from eight coal blend properties.

**Scientific Reference & Conceptual Framework:**  
P. S. Dash, M. Guha, D. Chakraborty, and P. K. Banerjee (2012). *Prediction of Coke CSR from Coal Blend Characteristics using Various Techniques: A Comparative Evaluation*. International Journal of Coal Preparation and Utilization, 32(4), 169–188. [DOI: 10.1080/19392699.2011.640301](https://www.tandfonline.com/doi/full/10.1080/19392699.2011.640301).

---

## 1. Project Overview & Objectives

In metallurgical blast-furnace coke-making, Coke Strength after Reaction (CSR) and Coke Reactivity Index (CRI) represent the premier indicators of high-temperature mechanical competence and resistance to chemical gasification by $\text{CO}_2$. Accurately predicting CSR and CRI from coal blend properties before carbonization in commercial coke ovens enables cost-effective blend optimization, conservation of premium coking coals, and mitigation of operational risks.

This research reproduction implements a rigorous, leak-free machine learning framework to evaluate how effectively four distinct regression paradigms learn the nonlinear mapping from eight coal blend characteristics to CSR and CRI:
1. **Multiple Linear Regression (MLR) — Phase 1 Baseline** (Standardized OLS with all 8 features)
2. **XGBoost Regressor** (Gradient-boosted decision trees with 5-fold cross-validation)
3. **Random Forest Regressor** (Bagged ensemble of decision trees with 5-fold cross-validation)
4. **Decision Tree Regressor** (Pruned single decision trees via cost-complexity pruning `ccp_alpha`)

---

## 2. Dataset Description

The experimental dataset comprises 68 commercial industrial coal blends.

### Input Features (8 Coal Blend Properties)
| Feature Name | Symbol / Code | Unit | Metallurgical Interpretation |
| :--- | :--- | :--- | :--- |
| **Ash Content** | `Ash` | % | Inorganic mineral residue remaining after complete coal combustion. |
| **Volatile Matter** | `VM` | % | Gaseous and liquid hydrocarbons evolved during coal pyrolysis. |
| **Mean Vitrinite Reflectance** | `Ro` | % | Fundamental optical measurement indicating coal rank/maturity. |
| **Vitrinite Distribution** | `V9_V13` | % | Proportion of reactive vitrinite macerals within V9 to V13 reflectance classes. |
| **Total Reactives** | `TR` | % | Sum of active, softening coal macerals (vitrinite + liptinite + reactive seminitrinite). |
| **Total Inerts** | `TI` | % | Unreactive refractory organic and inorganic constituents. |
| **Crucible Swelling Number** | `CSN` | Index | Caking ability and plastic expansion of coal upon rapid heating. |
| **Basicity Index** | `BI` | Ratio | Catalytic mineral ratio: $\frac{(\text{Fe}_2\text{O}_3 + \text{CaO} + \text{MgO} + \text{Na}_2\text{O} + \text{K}_2\text{O})}{(\text{SiO}_2 + \text{Al}_2\text{O}_3)} \times \text{Ash}$. |

### Target Variables (Independent Predictions)
| Target Variable | Symbol | Unit | Metallurgical Role |
| :--- | :--- | :--- | :--- |
| **Coke Strength after Reaction** | `CSR` | % | Mechanical abrasion strength of coke after high-temperature reaction with $\text{CO}_2$ at 1100 °C. (Higher is desirable, ideally $\ge 60\%$). |
| **Coke Reactivity Index** | `CRI` | % | Percentage mass loss of coke due to $\text{CO}_2$ gasification at 1100 °C. (Lower is desirable, ideally $\le 30\%$). |

---

## 3. Key Findings & Methodology Highlights

1. **Compositional Closure ($TR + TI \approx 100\%$):**
   - The empirical dataset confirms that $TR + TI = 100.006\% \pm 0.024\%$, establishing a Pearson correlation of $r = -0.99997$.
   - In the Phase 1 MLR model, this creates extreme multicollinearity with Variance Inflation Factors exceeding **18,700** and a condition number of $4.77 \times 10^5$.
   - While the in-sample training fit achieves $R^2 = 0.601$ for CSR, the model experiences extreme variance inflation, resulting in negative generalization scores on the independent test set.
2. **Nonlinear Tree Algorithms vs. Small Dataset Regime ($N=68$):**
   - **For CSR Prediction:** XGBoost demonstrated superior test set generalization, achieving a **Test RMSE of 5.51%** and **Test MAE of 3.79%**, significantly outperforming the unregularized Phase 1 MLR ($6.92\%$ RMSE).
   - **For CRI Prediction:** Random Forest achieved the most robust overall balance, delivering a **Test RMSE of 2.97%**, **Test MAE of 2.37%**, and the highest 5-fold cross-validation $R^2$ ($0.338 \pm 0.178$).
   - **Decision Tree:** While yielding fully transparent heuristic decision rules (e.g. splitting on Ash at $12.60\%$ and VM at $23.95\%$), single trees proved prone to high variance on the small test partition.
3. **Preservation of Suspicious Observations:**
   - In accordance with rigorous scientific practices, extreme blends (such as Blend #11 with CSR=18.8% and CRI=52.0%) were fully preserved to provide realistic and honest evaluations of real-world model deployment.

---

## 4. Directory Structure

```
COKE_QUALITY_PREDICTION/
├── data/
│   ├── raw/
│   │   └── coal_coke_data.csv          # Raw 68-blend dataset with headers
│   └── processed/
│       ├── cleaned_coal_coke.csv       # Standardized dataset
│       ├── train.csv                   # 80% Training partition (n=54)
│       ├── test.csv                    # 20% Independent test partition (n=14)
│       └── scaler.joblib               # StandardScaler fitted strictly on train
├── notebooks/
│   ├── 01_Data_Inspection.ipynb        # Ingestion, schema audit, dtypes
│   ├── 02_Data_Cleaning.ipynb          # Missingness, duplicates, TR+TI closure
│   ├── 03_Exploratory_Data_Analysis.ipynb # Univariate/bivariate stats & heatmaps
│   ├── 04_MLR_Phase1.ipynb             # Statsmodels OLS & collinearity diagnostics
│   ├── 05_XGBoost.ipynb                # Gradient boosted tree hyperparameter tuning
│   ├── 06_Random_Forest.ipynb          # Bagged random forest optimization
│   ├── 07_Decision_Tree.ipynb          # Pruned decision trees & rule extraction
│   ├── 08_Model_Comparison.ipynb       # Tabular comparative evaluation
│   └── 09_Explainability.ipynb         # SHAP, permutation, and MDI importances
├── src/
│   ├── data_preprocessing.py           # Ingestion, audit, and clean splitting
│   ├── eda.py                          # Statistical profiling, VIF, correlations
│   ├── mlr_model.py                    # Phase 1 MLR OLS modeling
│   ├── xgboost_model.py                # XGBoost modeling & SHAP computation
│   ├── random_forest_model.py          # Random Forest modeling & permutation
│   ├── decision_tree_model.py          # Decision Tree modeling & rule parsing
│   ├── evaluation.py                   # Multi-metric calculation engine
│   ├── visualization.py                # 300 DPI publication-grade plotting
│   └── prediction.py                   # Standalone inference engine CLI
├── models/
│   ├── csr/                            # Fitted CSR models & parameters
│   └── cri/                            # Fitted CRI models & parameters
├── results/
│   ├── graphs/                         # 30 High-resolution PNG figures (300 DPI)
│   ├── tables/                         # CSV and Excel comparative reports
│   └── predictions/                    # Batch prediction exports
├── reports/
│   └── Research_Report.md              # Academic-grade research manuscript
├── config.py                           # Central configuration & parameters
├── main.py                             # Master pipeline orchestrator
├── requirements.txt                    # Python library requirements
└── README.md                           # Documentation & execution guide
```

---

## 5. Installation & Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd c:\Users\ABHISHEK\OneDrive\Desktop\Project_btech
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 6. Execution Instructions

### A. Run Master Pipeline End-to-End
To run the complete data audit, EDA, model training, cross-validation, figure generation, and comparative reporting in a single command:
```bash
python main.py
```

### B. Interactive Prediction CLI
To predict CSR and CRI for any arbitrary coal blend:
```bash
# Predict with specific blend properties
python src/prediction.py --ash 13.5 --vm 22.8 --ro 1.15 --v9_v13 80.0 --tr 48.0 --ti 52.0 --csn 4.0 --bi 0.12

# Predict batch from a CSV file
python src/prediction.py --file data/processed/test.csv
```

### C. Run Individual Modeling Pipelines
```bash
python src/mlr_model.py
python src/xgboost_model.py
python src/random_forest_model.py
python src/decision_tree_model.py
```

---

## 7. Comparative Performance Summary

### CSR Prediction Performance (Test Set: $n=14$, CV: 5-Fold on Train $n=54$)
| Model | Test RMSE (%) | Test MAE (%) | Train $R^2$ | CV $R^2$ (Mean $\pm$ Std) | CV RMSE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Regressor** | **5.51** | **3.79** | 0.998 | $0.163 \pm 0.400$ | $6.23 \pm 2.31$ |
| **Random Forest Regressor** | 6.50 | 4.20 | 0.752 | $0.151 \pm 0.280$ | $6.49 \pm 2.35$ |
| **MLR Phase 1 Baseline** | 6.92 | 4.00 | 0.601 | $0.231 \pm 0.536$ | $5.77 \pm 2.25$ |
| **Decision Tree Regressor** | 8.56 | 5.62 | 0.917 | $-0.175 \pm 0.777$ | $6.64 \pm 2.30$ |

### CRI Prediction Performance (Test Set: $n=14$, CV: 5-Fold on Train $n=54$)
| Model | Test RMSE (%) | Test MAE (%) | Train $R^2$ | CV $R^2$ (Mean $\pm$ Std) | CV RMSE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Regressor** | **2.97** | **2.37** | 0.753 | **$0.338 \pm 0.178$** | $3.45 \pm 1.27$ |
| **XGBoost Regressor** | 3.31 | 2.87 | 0.856 | $0.270 \pm 0.306$ | $3.33 \pm 1.03$ |
| **Decision Tree Regressor** | 3.54 | 2.92 | 0.609 | $0.330 \pm 0.358$ | $3.27 \pm 1.12$ |
| **MLR Phase 1 Baseline** | 4.18 | 3.14 | 0.543 | $0.041 \pm 0.662$ | $3.69 \pm 0.98$ |

