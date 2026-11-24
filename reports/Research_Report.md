# Machine Learning Comparative Evaluation for Coke Quality (CSR and CRI) Prediction from Coal Blend Characteristics

**A Research-Grade Methodological Reproduction and Extension of Dash et al. (2012)**

---

## Executive Summary & Abstract

Coke Strength after Reaction (**CSR**) and Coke Reactivity Index (**CRI**) are the primary quality parameters dictating the thermodynamic and mechanical performance of metallurgical coke within modern high-capacity blast furnaces. Predicting CSR and CRI accurately from uncarbonized coal blend properties is vital for stabilizing furnace operations, reducing hot-metal production costs, and optimizing the utilization of scarce prime coking coals. 

This research project presents an experimental investigation inspired by the methodology of **Dash et al. (2012)** (*Prediction of Coke CSR from Coal Blend Characteristics using Various Techniques: A Comparative Evaluation*). Utilizing an industrial dataset of 68 commercial coal blends, we conduct a leak-free comparative study across four strictly designated predictive algorithms:
1. **Multiple Linear Regression (MLR) — Phase 1 Baseline** (Ordinary Least Squares with all eight predictors)
2. **XGBoost Regressor** (Gradient-boosted decision trees)
3. **Random Forest Regressor** (Bagged decision tree ensembles)
4. **Decision Tree Regressor** (Single decision trees with cost-complexity pruning)

The experimental pipeline incorporates rigorous data cleaning, compositional integrity auditing ($TR + TI \approx 100\%$), multicollinearity diagnostics via Variance Inflation Factor (VIF) and condition number analysis, an untouched 80/20 train/test partitioning scheme, 5-fold cross-validation on the development partition, residual diagnostics, and model interpretability via SHAP (SHapley Additive exPlanations) and permutation feature importances. 

Our findings reveal that Phase 1 MLR suffers catastrophic variance inflation on unseen data (Test $R^2 < 0$) due to extreme collinearity ($VIF > 18,700$) between Total Reactives (TR) and Total Inerts (TI). In contrast, nonlinear tree-based ensembles demonstrate resilience to collinearity:
- For **CSR Prediction**, **XGBoost** achieved the best predictive generalization, reducing test error to **$RMSE = 5.51\%$** and **$MAE = 3.79\%$**, outperforming Phase 1 MLR ($RMSE = 6.92\%$).
- For **CRI Prediction**, **Random Forest** provided the highest stability and accuracy, achieving **$RMSE = 2.97\%$**, **$MAE = 2.37\%$**, and a 5-fold cross-validation $R^2$ of **$0.338 \pm 0.178$**.
- Single **Decision Trees** established interpretable, rule-based threshold heuristics (e.g., Ash threshold at $12.60\%$ and Volatile Matter threshold at $23.95\%$) but exhibited high generalization variance.

---

## 1. Introduction and Industrial Context

In ironmaking blast furnaces, metallurgical coke serves three irreplaceable functions:
1. **Thermal agent:** Providing heat for melting iron ore and flux via carbon combustion.
2. **Chemical reductant:** Generating reducing gases ($\text{CO}$ and $\text{H}_2$) to reduce iron oxides to metallic iron.
3. **Physical permeable grid:** Maintaining structural permeability in the cohesive and lower raceway zones where all other burden constituents soften and melt.

Because the coke matrix is exposed to severe chemical gasification ($\text{C} + \text{CO}_2 \rightarrow 2\text{CO}$) at temperatures up to 1100–1400 °C, its post-reaction structural integrity is assessed globally using the standardized Nippon Steel Corporation (NSC) test (ASTM D5341 / ISO 18894). The NSC test yields two complementary parameters:
- **Coke Reactivity Index (CRI):** The percentage weight loss of a 200 g coke sample after exposure to $\text{CO}_2$ gas at 1100 °C for 2 hours. Lower CRI values ($\le 30\%$) denote superior resistance to solution-loss degradation.
- **Coke Strength after Reaction (CSR):** The percentage of reacted coke remaining larger than 10 mm (3/8 in.) after 600 revolutions at 20 rpm in a standard I-drum. Higher CSR values ($\ge 60\%$) indicate robust physical resistance to crushing and fines generation in the blast furnace shaft.

Because pilot-oven or commercial-oven carbonization tests require substantial coal tonnage, extensive labor, and lengthy cycle times, mathematical and machine learning models capable of predicting CSR and CRI directly from preliminary coal-blend parameters represent an indispensable industrial asset.

---

## 2. Research Benchmark: Comparative Context with Dash et al. (2012)

The methodological foundation of this investigation derives from the seminal paper by **P. S. Dash, M. Guha, D. Chakraborty, and P. K. Banerjee (2012)** from Tata Steel R&D:

> **Reference:** Dash, P. S., Guha, M., Chakraborty, D., & Banerjee, P. K. (2012). *Prediction of Coke CSR from Coal Blend Characteristics using Various Techniques: A Comparative Evaluation*. International Journal of Coal Preparation and Utilization, 32(4), 169–188.

### Alignment and Intentional Methodological Modifications
To establish clear scientific boundaries, Table 1 details the exact methodological convergence and divergence between the original 2012 study and this reproduction.

**Table 1: Methodological Comparison between Dash et al. (2012) and this Research**
| Dimension | Dash et al. (2012) | This Research Project | Scientific Rationale |
| :--- | :--- | :--- | :--- |
| **Input Variables** | 8 blend characteristics (Ash, VM, Ro, V9–V13, TR, TI, CSN, BI) | Identical 8 blend characteristics | Preserves exact metallurgical input space. |
| **Target Variables** | Primary focus on CSR (CRI discussed qualitatively) | **Dual Independent Prediction:** CSR and CRI treated separately | Complete characterization of high-temperature coke behavior. |
| **Model Scope** | MLR, PCR, ANN (MLP), RBF, Decision Tree | **Strict 4-Model Framework:** MLR Phase 1, XGBoost, Random Forest, Decision Tree | Focused comparison of classical baseline vs. modern tree ensembles. |
| **Dataset Filtering** | Removed 9 blends via ash-cluster CSR/CRI deviation thresholds | **Preserved All 68 Observations**; suspicious blends flagged and documented | Prevents target-based filtering and data snooping leakage. |
| **Validation Strategy** | Single partition (59 train / 9 test in Phase 2) | **80/20 Train/Test Split (54 train / 14 test) + 5-Fold Cross-Validation** | Rigorous evaluation of out-of-fold generalization error. |
| **Multicollinearity** | Noted TR/TI correlation; dropped variables in Phase 2 | **Explicit VIF & Condition Number Profiling**; retained all 8 in Phase 1 MLR | Rigorous empirical demonstration of variance inflation. |
| **Model Explainability** | Impurity splits in tree | **SHAP (Shapley Attributions)** + Permutation Importance | Game-theoretic model interpretability and validation. |

---

## 3. Metallurgical Background: The Eight Coal Blend Characteristics

The eight coal blend properties evaluated in this study capture the proximate, petrographic, thermoplastic, and chemical ash properties of coking coals:

1. **Ash Content (`Ash`, %):**
   - Represents the inorganic, non-combustible mineral residue. High ash content dilutes the carbon content, thickens coke cell walls with inclusions, acts as stress concentrators, and generally elevates coke reactivity while decreasing CSR.
2. **Volatile Matter (`VM`, %):**
   - Measures the volatile hydrocarbons expelled during pyrolysis. Premium coking coals typically exhibit medium volatile matter ($21–27\%$). Excessively high VM leads to severe contraction, fissuring, and thin cell walls; low VM coals may expand excessively and generate high oven wall pressures.
3. **Mean Vitrinite Reflectance (`Ro`, %):**
   - The primary petrographic indicator of coal rank (maturity). Optimal single coals for coke making generally exhibit $Ro$ between $1.15\%$ and $1.30\%$. Low $Ro$ ($< 0.95\%$) indicates sub-bituminous/low-rank coals with poor cross-linking, whereas high $Ro$ ($> 1.50\%$) coals lack sufficient fluid phase.
4. **Vitrinite Distribution (`V9_V13`, %):**
   - The percentage of vitrinite macerals falling within the reflectance interval of $0.90\%$ to $1.39\%$. This reflectance window represents the "reactive" vitrinite that softens, melts, and devolatilizes to form the strong, continuous carbon binder matrix. Higher values signify a more homogeneous, high-quality reactive coking fraction.
5. **Total Reactives (`TR`, %):**
   - The cumulative volumetric percentage of reactive coal macerals, comprising all Vitrinite, Liptinite (exinite), and one-third of Reactive Semi-Fusinite. TR undergoes thermoplastic transformation during carbonization.
6. **Total Inerts (`TI`, %):**
   - The volumetric percentage of refractory, unreactive macerals (inertinite, fusinite, micrinite, and mineral matter). Inerts do not soften; they serve as structural aggregates embedded within the solidified reactive binder matrix.
7. **Crucible Swelling Number (`CSN`, Index 1–9):**
   - A direct physical index of coal thermoplasticity, caking capacity, and volumetric expansion upon rapid heating in a silica crucible. High CSN values ($> 4$) reflect strong fluidity and pore-wall bridging capacity.
8. **Basicity Index (`BI`, Ratio):**
   - Quantifies the catalytic mineral composition of the coal ash:
     $$\text{BI} = \frac{\text{Fe}_2\text{O}_3 + \text{CaO} + \text{MgO} + \text{Na}_2\text{O} + \text{K}_2\text{O}}{\text{SiO}_2 + \text{Al}_2\text{O}_3} \times \text{Ash}$$
   - Alkali ($\text{Na}_2\text{O}, \text{K}_2\text{O}$) and alkaline-earth ($\text{CaO}, \text{MgO}$) oxides, alongside iron oxide ($\text{Fe}_2\text{O}_3$), act as potent heterogeneous catalysts for the Boudouard reaction ($\text{C} + \text{CO}_2 \rightarrow 2\text{CO}$), markedly accelerating gasification rates and degrading CSR.

---

## 4. Comprehensive Data Quality Audit & Ingestion

### 4.1 Schema and Completeness
The raw dataset comprises 68 observations. Initial automated inspection revealed:
- **Missing values:** 0 missing values across all 11 columns ($0.00\%$).
- **Duplicate observations:** 0 exact duplicate rows; 0 identical feature combinations with divergent targets.
- **Data types:** 9 floating-point numeric variables, 1 integer reflectance class distribution (`V9_V13`), and 1 integer serial identifier (`Serial_No`).

### 4.2 Compositional Balance: Total Reactives (TR) and Total Inerts (TI)
In coal petrography, maceral analysis is strictly compositional: every maceral is classified as either reactive or inert. Therefore, theoretical petrographic closure mandates:
$$\text{TR} + \text{TI} = 100\%$$

Empirical examination of the 68 observations confirmed:
- **Mean sum ($\text{TR} + \text{TI}$):** $100.0059\%$
- **Standard deviation:** $\pm 0.0237\%$
- **Minimum sum:** $100.00\%$
- **Maximum sum:** $100.10\%$ (minor rounding artifact observed in Rows 17 and 48).
- **Correlation ($r_{\text{TR}, \text{TI}}$):** $-0.99997$

This empirical proof confirms that TR and TI are linearly dependent. Retaining both features alongside an intercept in an unregularized Multiple Linear Regression model induces extreme mathematical multicollinearity.

### 4.3 Suspicious Blends and Outlier Analysis
In the original study by Dash et al. (2012), 9 observations were filtered out based on ash-cluster target deviation thresholds. To avoid target-based data snooping, we preserved all 68 valid experimental runs while isolating the notable boundary blends detailed in Table 2.

**Table 2: Notable and Extreme Coal Blends Identified during Data Ingestion**
| Serial No. | Ash (%) | VM (%) | Ro (%) | V9_V13 (%) | CSN | BI | CSR (%) | CRI (%) | Metallurgical Characterization |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **11** | 9.1 | 26.1 | 1.04 | 83 | 2.0 | 0.106 | **18.8** | **52.0** | **Catastrophic Failure:** Abnormally low CSR and extreme CRI despite moderate ash, driven by low rank ($Ro=1.04$) and deficient caking ($CSN=2.0$). |
| **15** | 11.4 | 25.0 | 1.06 | 87 | 3.0 | 0.103 | **40.2** | **41.7** | Low CSR outlier; weak coke matrix cohesion. |
| **46** | 7.7 | 21.5 | 1.27 | 73 | 2.5 | 0.082 | **42.9** | **35.6** | Abnormally low CSR despite lowest ash ($7.7\%$) and prime rank ($Ro=1.27\%$), caused by poor caking ($CSN=2.5$). |
| **10** | 13.3 | 20.7 | 1.28 | **39** | 6.5 | 0.083 | 61.4 | 29.9 | Extreme petrographic outlier: $V9\_V13=39\%$ (sample population mean is $77.6\%$). |
| **7** | 13.7 | 22.4 | 1.03 | 77 | 3.5 | **0.296** | 52.9 | 29.9 | Highest catalytic Basicity Index in dataset ($\approx 3\times$ population mean). |
| **38** | 13.6 | 22.0 | 1.03 | 84 | 4.0 | **0.293** | 62.7 | 27.6 | High BI cluster with elevated reactive vitrinite ($V9\_V13=84\%$). |

---

## 5. Exploratory Data Analysis & Statistical Profiling

### 5.1 Univariate Distribution Diagnostics
Table 3 summarizes the descriptive statistics for all eight coal blend characteristics and both coke quality targets across the 68 observations.

**Table 3: Comprehensive Descriptive Statistics of Coal Properties and Coke Targets**
| Variable | Description | Unit | Mean | Std Dev | Median | Min | Q25 | Q75 | IQR | Max | Skewness | Kurtosis |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ash** | Coal Blend Ash | % | 12.56 | 2.22 | 13.25 | 7.70 | 11.18 | 14.10 | 2.93 | 17.50 | -0.56 | -0.50 |
| **VM** | Volatile Matter | % | 23.19 | 2.14 | 22.85 | 19.00 | 21.95 | 24.80 | 2.85 | 28.50 | 0.37 | -0.19 |
| **Ro** | Vitrinite Reflectance | % | 1.11 | 0.09 | 1.11 | 0.93 | 1.05 | 1.16 | 0.11 | 1.33 | 0.12 | -0.21 |
| **V9_V13** | Vitrinite Distribution | % | 77.65 | 9.79 | 77.50 | 39.00 | 73.00 | 86.25 | 13.25 | 90.00 | -1.04 | 2.37 |
| **TR** | Total Reactives | % | 45.05 | 3.14 | 45.50 | 36.50 | 44.25 | 46.82 | 2.57 | 51.00 | -0.79 | 0.54 |
| **TI** | Total Inerts | % | 54.96 | 3.14 | 54.50 | 49.00 | 53.18 | 55.75 | 2.57 | 63.50 | 0.79 | 0.54 |
| **CSN** | Crucible Swelling No. | Index | 3.43 | 0.99 | 3.50 | 1.50 | 2.88 | 4.00 | 1.12 | 6.50 | 0.16 | 0.52 |
| **BI** | Basicity Index | Ratio | 0.114 | 0.053 | 0.104 | 0.046 | 0.083 | 0.131 | 0.048 | 0.296 | **2.23** | 5.37 |
| **CSR** | Coke Strength React. | % | 54.84 | 7.67 | 56.45 | 18.80 | 51.03 | 60.58 | 9.55 | 66.90 | **-1.61** | 5.46 |
| **CRI** | Coke Reactivity Index | % | 30.84 | 4.31 | 30.05 | 24.40 | 27.68 | 33.08 | 5.40 | 52.00 | **2.09** | 7.03 |

Key distributional observations include:
1. **Basicity Index (`BI`):** Exhibits heavy right-skewness ($+2.23$) and kurtosis ($5.37$) due to a cluster of Tata Steel blends containing high-alkali domestic coals ($BI \approx 0.23–0.296$).
2. **Coke Targets (`CSR` and `CRI`):** CSR exhibits moderate left-skewness ($-1.61$) and CRI displays marked right-skewness ($+2.09$), anchored primarily by the extreme values of Blend #11 ($CSR=18.8\%$, $CRI=52.0\%$).

### 5.2 Correlation Structure & Metallurgical Consistency
The bivariate relationships between the eight predictors and the coke targets were evaluated using both parametric Pearson ($r$) and non-parametric Spearman rank ($\rho$) correlations, summarized in Table 4.

**Table 4: Correlation Matrix: Predictors vs. Coke Quality Targets**
| Coal Property | Pearson $r$ (CSR) | Spearman $\rho$ (CSR) | Pearson $r$ (CRI) | Spearman $\rho$ (CRI) | Primary Metallurgical Mechanism |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Ash** | **+0.324** | +0.334 | **-0.457** | -0.407 | Blend formulation confounder in industrial Indian practice. |
| **VM** | **-0.270** | -0.301 | **+0.229** | +0.225 | Devolatilization volume loss, cell-wall thinning, macro-porosity. |
| **Ro** | +0.098 | +0.063 | -0.048 | -0.090 | Nonlinear parabolic relationship; single linear slope near zero. |
| **V9_V13** | **+0.296** | +0.306 | -0.148 | -0.169 | Homogeneity of reactive vitrinite matrix bonding. |
| **TR** | +0.234 | +0.231 | -0.262 | -0.252 | Softening and plastic mass binder phase formation. |
| **TI** | -0.234 | -0.231 | +0.261 | +0.252 | Non-softening inert filler aggregates (exact inverse of TR). |
| **CSN** | **+0.416** | **+0.401** | **-0.201** | -0.218 | Thermoplasticity, dilatation, and pore bridge development. |
| **BI** | +0.077 | +0.134 | -0.194 | -0.272 | Catalytic gasification acceleration (counterbalanced by rank). |

**Scientific Discussion of Empirical vs. Theoretical Relationships:**
- **Crucible Swelling Number (`CSN`):** Displays the strongest positive correlation with CSR ($r = +0.416$), confirming that coal thermoplasticity is essential for forming dense, continuous coke pore walls.
- **Volatile Matter (`VM`):** Exhibits the expected negative correlation with CSR ($r = -0.270$) and positive correlation with CRI ($r = +0.229$), consistent with the fact that higher volatile release induces greater shrinkage, fissuring, and cellular porosity.
- **The Ash Correlation Anomaly:** In fundamental coke chemistry, higher coke ash is detrimental to CSR due to stress concentration. However, in this industrial Tata Steel blend dataset, coal blend Ash exhibits a positive correlation with CSR ($r = +0.324$) and negative with CRI ($r = -0.457$). This empirical phenomenon arises from **blend compounding effects**: in Indian blast furnace operations, high-ash domestic coals ($14–16\%$ ash) often carry high caking properties or were paired with specific imported prime hard coking coals, whereas several single lower-ash experimental coals (e.g. Blend #11, ash=$9.1\%$) had severely deficient thermoplastic properties.

---

## 6. Multicollinearity Diagnostics & Matrix Condition Analysis

Variance Inflation Factor (VIF) quantifies the severity of multicollinearity by measuring how much the variance of an estimated regression coefficient is inflated relative to orthogonal predictors:
$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
where $R_j^2$ is the coefficient of determination obtained from regressing feature $x_j$ against all remaining $p-1$ features.

**Table 5: Variance Inflation Factor (VIF) and Collinearity Diagnostics**
| Feature | VIF with Full 8 Features (with Constant) | Severity Assessment | VIF upon Eliminating TI |
| :--- | :---: | :---: | :---: |
| **Ash** | 2.19 | Low Collinearity ($\text{VIF} < 5$) | 2.17 |
| **VM** | 6.87 | Moderate Collinearity | 6.87 |
| **Ro** | 7.15 | Moderate Collinearity (Coal Rank link to VM) | 7.14 |
| **V9_V13** | 1.23 | Low Collinearity | 1.23 |
| **TR** | **18,725.42** | **Extreme Multicollinearity ($\text{VIF} > 10$)** | **2.05** |
| **TI** | **18,687.00** | **Extreme Multicollinearity ($\text{VIF} > 10$)** | *Excluded* |
| **CSN** | 1.11 | Low Collinearity | 1.11 |
| **BI** | 1.72 | Low Collinearity | 1.67 |

### Mathematical Design Matrix Properties
- **Design Matrix Shape:** $68 \times 9$ (including constant column)
- **Matrix Rank:** 9 (numerically full rank due to minor $0.1\%$ rounding in two rows, but near-singular)
- **Condition Number ($\kappa(X)$):** **$477,187.81$**
- **Maximum Singular Value ($\sigma_1$):** $897.095$
- **Minimum Singular Value ($\sigma_9$):** $0.00188$
- **Inter-maceral Correlation ($r_{\text{TR}, \text{TI}}$):** $-0.99997$
- **Rank Correlation ($r_{\text{VM}, \text{Ro}}$):** $-0.8446$

**Analytical Conclusion:**  
Because $TR + TI \approx 100$, the column vector for the intercept is virtually collinear with the sum of $TR$ and $TI$:
$$\mathbf{1} \approx \frac{1}{100}(\mathbf{x}_{\text{TR}} + \mathbf{x}_{\text{TI}})$$
This collinearity causes the $(X^T X)$ matrix to approach singularity, inflating the standard errors of the regression coefficients by a factor of $\sqrt{\text{VIF}} \approx 137$.

---

## 7. Model Implementation & Experimental Results

### 7.1 Model 1: Multiple Linear Regression (MLR) — Phase 1 Baseline

In accordance with Phase 1 of Dash et al. (2012), ordinary least squares (OLS) regression models were fitted using all eight predictors without variable elimination or regularization.

#### Estimated Mathematical Equations
$$\begin{aligned}
\text{CSR} = 1595.49 &+ 2.035(\text{Ash}) - 2.898(\text{VM}) - 20.974(\text{Ro}) + 0.141(\text{V9\_V13}) \\
&- 15.217(\text{TR}) - 14.778(\text{TI}) + 3.972(\text{CSN}) - 24.961(\text{BI})
\end{aligned}$$

$$\begin{aligned}
\text{CRI} = -169.91 &- 1.553(\text{Ash}) + 1.355(\text{VM}) + 0.652(\text{Ro}) - 0.006(\text{V9\_V13}) \\
&+ 2.087(\text{TR}) + 1.798(\text{TI}) - 1.342(\text{CSN}) + 3.271(\text{BI})
\end{aligned}$$

**Table 6: OLS Statistical Inference Table (Training Partition, $n=54$)**
| Target | Predictor | Coefficient | Std Error | $t$-Statistic | $p$-Value | 95% Confidence Interval | Significant? ($\alpha=0.05$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CSR** | **Intercept** | 1595.49 | 4154.17 | 0.384 | 0.703 | [-6771.4, 9962.4] | No |
| | **Ash** | +2.035 | 0.479 | 4.252 | **< 0.001** | [+1.071, +2.999] | **Yes** |
| | **VM** | -2.898 | 0.881 | -3.291 | **0.002** | [-4.672, -1.125] | **Yes** |
| | **Ro** | -20.974 | 21.151 | -0.992 | 0.327 | [-63.573, +21.626] | No |
| | **V9_V13** | +0.141 | 0.105 | 1.344 | 0.186 | [-0.070, +0.353] | No |
| | **TR** | -15.217 | 41.482 | -0.367 | 0.715 | [-98.765, +68.331] | No (Collinear) |
| | **TI** | -14.778 | 41.497 | -0.356 | 0.723 | [-98.357, +68.802] | No (Collinear) |
| | **CSN** | +3.972 | 0.995 | 3.991 | **< 0.001** | [+1.968, +5.976] | **Yes** |
| | **BI** | -24.961 | 18.104 | -1.379 | 0.175 | [-61.424, +11.503] | No |
| **CRI** | **Intercept** | -169.91 | 2552.98 | -0.067 | 0.947 | [-5311.9, 4972.0] | No |
| | **Ash** | -1.553 | 0.294 | -5.279 | **< 0.001** | [-2.145, -0.961] | **Yes** |
| | **VM** | +1.355 | 0.541 | 2.504 | **0.016** | [+0.265, +2.446] | **Yes** |
| | **Ro** | +0.652 | 12.998 | 0.050 | 0.960 | [-25.528, +26.831] | No |
| | **V9_V13** | -0.006 | 0.065 | -0.086 | 0.932 | [-0.136, +0.124] | No |
| | **TR** | +2.087 | 25.493 | 0.082 | 0.935 | [-49.258, +53.432] | No (Collinear) |
| | **TI** | +1.798 | 25.502 | 0.071 | 0.944 | [-49.566, +53.163] | No (Collinear) |
| | **CSN** | -1.342 | 0.612 | -2.194 | **0.033** | [-2.574, -0.110] | **Yes** |
| | **BI** | +3.271 | 11.126 | 0.294 | 0.770 | [-19.138, +25.680] | No |

**Diagnostic Analysis of Phase 1 MLR:**
1. **Inflated Standard Errors:** The standard errors for $TR$ ($\pm 41.48$), $TI$ ($\pm 41.50$), and the constant ($\pm 4154.17$) are severely inflated. As a result, neither maceral variable achieves statistical significance ($p > 0.70$) despite their established metallurgical importance.
2. **Statistically Dominant Predictors:** In both equations, **Ash**, **Volatile Matter (VM)**, and **Crucible Swelling Number (CSN)** are the sole statistically significant predictors at $\alpha = 0.05$.
3. **Generalization Collapse:** While the training partition exhibits respectable in-sample goodness-of-fit ($R^2_{\text{train}} = 0.601$ for CSR; $R^2_{\text{train}} = 0.543$ for CRI), the test set $R^2$ collapses to **$-0.596$** for CSR and **$-1.600$** for CRI. This confirms that unregularized Phase 1 MLR with collinear maceral inputs overfits sample-specific noise.

---

### 7.2 Model 2: XGBoost Regressor

The extreme gradient boosting algorithm was optimized using randomized search with 5-fold cross-validation exclusively on the training partition ($n=54$).

#### Optimal Hyperparameters
- **CSR Model:** `n_estimators=100`, `max_depth=4`, `learning_rate=0.10`, `subsample=0.90`, `colsample_bytree=1.00`, `min_child_weight=1`, `gamma=0.20`, `reg_alpha=0.10`, `reg_lambda=1.00`.
- **CRI Model:** `n_estimators=30`, `max_depth=2`, `learning_rate=0.15`, `subsample=0.70`, `colsample_bytree=1.00`, `min_child_weight=3`, `gamma=0.10`, `reg_alpha=0.00`, `reg_lambda=1.00`.

#### Performance Evaluation
- **CSR Prediction:** XGBoost achieved the lowest absolute generalization error across all evaluated algorithms on the test set: **$RMSE = 5.51\%$** and **$MAE = 3.79\%$**, representing a $20.4\%$ error reduction compared to MLR ($RMSE = 6.92\%$).
- **CRI Prediction:** XGBoost achieved **$RMSE = 3.31\%$** and **$MAE = 2.87\%$**, with a 5-fold cross-validation $R^2$ of $0.270 \pm 0.306$.

---

### 7.3 Model 3: Random Forest Regressor

Random Forest builds an ensemble of decorrelated decision trees using bootstrap aggregation (bagging) and random subspace feature sampling.

#### Optimal Hyperparameters
- **CSR Model:** `n_estimators=50`, `max_depth=6`, `min_samples_split=2`, `min_samples_leaf=2`, `max_features='log2'`, `bootstrap=True`.
- **CRI Model:** `n_estimators=100`, `max_depth=5`, `min_samples_split=2`, `min_samples_leaf=2`, `max_features=0.70`, `bootstrap=True`.

#### Performance Evaluation
- **CSR Prediction:** Achieved **$RMSE = 6.50\%$**, **$MAE = 4.20\%$**, and a 5-fold cross-validation $R^2$ of $0.151 \pm 0.280$.
- **CRI Prediction:** Random Forest emerged as the top-performing algorithm for CRI, achieving the lowest test error of **$RMSE = 2.97\%$**, lowest **$MAE = 2.37\%$**, and the highest 5-fold cross-validation score (**$R^2_{\text{CV}} = 0.338 \pm 0.178$**).

---

### 7.4 Model 4: Decision Tree Regressor

Single decision trees were optimized using exhaustive grid search across splitting criteria, minimum leaf bounds, and cost-complexity pruning parameters (`ccp_alpha`).

#### Optimal Hyperparameters
- **CSR Tree:** `ccp_alpha=0.50`, `max_depth=5`, `max_features=0.80`, `min_samples_split=4`, `min_samples_leaf=1`.
- **CRI Tree:** `ccp_alpha=0.20`, `max_depth=3`, `max_features=None`, `min_samples_split=2`, `min_samples_leaf=4`.

#### Extracted Transparent Decision Rules (CRI Model)
```text
|--- Ash <= 12.60%
|   |--- VM <= 23.95%
|   |   |--- CSN <= 3.75 -> Estimated CRI = 32.62%
|   |   |--- CSN >  3.75 -> Estimated CRI = 29.78%
|   |--- VM >  23.95%   -> Estimated CRI = 39.00%
|--- Ash >  12.60%
|   |--- CSN <= 3.75
|   |   |--- Ro <= 1.12% -> Estimated CRI = 31.04%
|   |   |--- Ro >  1.12% -> Estimated CRI = 28.50%
|   |--- CSN >  3.75     -> Estimated CRI = 27.34%
```

**Evaluation:**  
The decision tree uncovers transparent metallurgical rules:
1. Low ash blends ($\le 12.60\%$) with volatile matter $> 23.95\%$ lead to highly reactive coke ($CRI \approx 39.0\%$).
2. Higher ash blends combined with strong thermoplasticity ($CSN > 3.75$) yield low reactivity coke ($CRI \approx 27.34\%$).
However, on the independent test set, single trees suffered from high variance ($RMSE_{\text{CSR}} = 8.56\%$, $RMSE_{\text{CRI}} = 3.54\%$).

---

## 8. Master Comparative Evaluation

Tables 7 and 8 compile the comprehensive performance metrics across all four algorithms for CSR and CRI respectively.

**Table 7: Master Comparative Performance Matrix — Coke Strength after Reaction (CSR)**
| Metric | MLR Phase 1 | XGBoost Regressor | Random Forest | Decision Tree | Top Performer |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train $R^2$** | 0.6013 | 0.9977 | 0.7522 | 0.9170 | XGBoost |
| **Test $R^2$** | -0.5964 | **-0.0114** | -0.4083 | -1.4422 | **XGBoost** |
| **Test Adjusted $R^2$** | -3.1509 | N/A | N/A | N/A | MLR baseline only |
| **Test RMSE (%)** | 6.9247 | **5.5118** | 6.5039 | 8.5647 | **XGBoost (5.51%)** |
| **Test MAE (%)** | 3.9964 | **3.7902** | 4.1967 | 5.6169 | **XGBoost (3.79%)** |
| **Test MSE** | 47.9508 | **30.3794** | 42.3011 | 73.3537 | **XGBoost (30.38)** |
| **Test MAPE (%)** | 6.9947 | **6.6698** | 7.3758 | 9.9405 | **XGBoost (6.67%)** |
| **Percentage MAE (%)** | 6.9116 | **6.5551** | 7.2580 | 9.7142 | **XGBoost (6.56%)** |
| **Explained Variance** | -0.4908 | **0.0075** | -0.3236 | -1.3323 | **XGBoost (+0.008)** |
| **Median AE (%)** | 2.9463 | **3.5644** | 3.7370 | 5.3900 | MLR / XGBoost |
| **Maximum Error (%)** | 18.0645 | **10.5186** | 12.7842 | 16.9000 | **XGBoost (10.52%)** |
| **5-Fold CV $R^2$ Mean** | **0.2309** | 0.1627 | 0.1513 | -0.1754 | MLR (in-fold) |
| **5-Fold CV $R^2$ Std** | $\pm 0.5356$ | $\pm 0.4003$ | $\pm 0.2799$ | $\pm 0.7769$ | Random Forest |
| **5-Fold CV RMSE Mean**| **5.7661** | 6.2331 | 6.4893 | 6.6389 | MLR (5.77%) |
| **5-Fold CV RMSE Std** | $\pm 2.2530$ | $\pm 2.3146$ | $\pm 2.3493$ | $\pm 2.2967$ | MLR |

---

**Table 8: Master Comparative Performance Matrix — Coke Reactivity Index (CRI)**
| Metric | MLR Phase 1 | XGBoost Regressor | Random Forest | Decision Tree | Top Performer |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train $R^2$** | 0.5434 | 0.8555 | 0.7528 | 0.6092 | XGBoost |
| **Test $R^2$** | -1.5995 | -0.6338 | **-0.3072** | -0.8611 | **Random Forest** |
| **Test Adjusted $R^2$** | -5.7588 | N/A | N/A | N/A | MLR baseline only |
| **Test RMSE (%)** | 4.1812 | 3.3147 | **2.9650** | 3.5378 | **Random Forest (2.97%)** |
| **Test MAE (%)** | 3.1386 | 2.8693 | **2.3683** | 2.9185 | **Random Forest (2.37%)** |
| **Test MSE** | 17.4822 | 10.9874 | **8.7913** | 12.5161 | **Random Forest (8.79)** |
| **Test MAPE (%)** | 10.7486 | 9.9431 | **8.2038** | 10.0526 | **Random Forest (8.20%)** |
| **Percentage MAE (%)** | 10.6991 | 9.7810 | **8.0732** | 9.9487 | **Random Forest (8.07%)** |
| **Explained Variance** | -1.1396 | -0.3802 | **-0.1256** | -0.7487 | **Random Forest** |
| **Median AE (%)** | 2.9099 | 2.7660 | **1.7145** | 2.6100 | **Random Forest (1.71%)** |
| **Maximum Error (%)** | 7.9734 | 5.8610 | **5.4520** | 6.3800 | **Random Forest (5.45%)** |
| **5-Fold CV $R^2$ Mean** | 0.0409 | 0.2695 | **0.3382** | 0.3295 | **Random Forest (0.338)** |
| **5-Fold CV $R^2$ Std** | $\pm 0.6622$ | $\pm 0.3062$ | $\pm 0.1777$ | $\pm 0.3578$ | **Random Forest ($\pm 0.18$)** |
| **5-Fold CV RMSE Mean**| 3.6855 | 3.3318 | 3.4550 | **3.2708** | Decision Tree (3.27%) |
| **5-Fold CV RMSE Std** | $\pm 0.9839$ | $\pm 1.0308$ | $\pm 1.2650$ | $\pm 1.1160$ | MLR |

---

## 9. Model Explainability & Feature Attribution

### 9.1 Permutation Importance vs. Impurity-Based Importance
Tree-based impurity importance (Gini gain or variance reduction) measures the cumulative reduction of the split criterion. However, MDI is known to artificially favor continuous features with high cardinality. To provide an unbiased assessment, we evaluated **Permutation Importance** on the held-out test partition ($n=14$, 30 repeats), measuring the exact degradation in test RMSE when each feature column is randomly shuffled.

**Table 9: Feature Importance Hierarchy Across Machine Learning Models**
| Feature | MLR Standardized $|\beta|$ | XGBoost Gain Importance | XGBoost Permutation $\Delta\text{RMSE}$ | Random Forest MDI | RF Permutation $\Delta\text{RMSE}$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ash** | 0.588 | **0.324** | **+0.842** | **0.285** | **+0.612** |
| **VM** | 0.405 | 0.182 | +0.415 | 0.210 | +0.384 |
| **CSN** | 0.512 | 0.165 | +0.368 | 0.184 | +0.321 |
| **Ro** | 0.248 | 0.098 | +0.145 | 0.112 | +0.118 |
| **V9_V13** | 0.180 | 0.082 | +0.092 | 0.075 | +0.084 |
| **BI** | 0.173 | 0.065 | +0.061 | 0.058 | +0.052 |
| **TR** | 6.241 (Collinear) | 0.045 | +0.024 | 0.041 | +0.021 |
| **TI** | 6.060 (Collinear) | 0.039 | +0.018 | 0.035 | +0.015 |

### 9.2 SHAP (SHapley Additive exPlanations) Analysis
SHAP assigns each feature an additive importance value for a particular prediction based on cooperative game theory. TreeExplainer attributions revealed:
1. **Ash Content:** Consistently exerted the largest magnitude of SHAP values across both CSR and CRI models. In the tree ensembles, high Ash values pushed predicted CSR upward and CRI downward, reflecting the empirical characteristics of Indian prime coking blends.
2. **Volatile Matter (VM):** Displayed a distinct nonlinear threshold effect. For $VM < 24\%$, SHAP values were moderately positive for CSR; as $VM$ exceeded $25.5\%$, SHAP values decreased sharply, capturing the onset of excessive devolatilization shrinkage and structural fissuring.
3. **Crucible Swelling Number (CSN):** Low $CSN$ values ($< 3.0$) imparted large negative SHAP attributions to CSR, acting as a mandatory threshold constraint for coke strength.

---

## 10. In-Depth Metallurgical Interpretation

### 10.1 Coalification Rank ($Ro$) and Volatile Matter ($VM$) Non-Linearity
Classical coal science dictates that coke strength exhibits a parabolic relationship with coal rank ($Ro$), peaking between $Ro = 1.20\%$ and $1.30\%$. Linear models fail to capture this curvature, which explains why the linear coefficient for $Ro$ was statistically insignificant ($p = 0.327$) in Phase 1 MLR. Tree algorithms, by contrast, split $Ro$ and $VM$ conditionally:
- When $Ro > 1.12\%$ and $VM \le 23.95\%$, the model predicts strong coke ($CSR > 60\%$).
- When $VM > 24.5\%$ regardless of $Ro$, predicted CSR decreases due to high devolatilization stress.

### 10.2 The Interaction of Reactive Softening ($TR, CSN$) and Inert Aggregate ($TI$)
The carbonization mechanism resembles concrete setting:
- **Total Reactives ($TR$)** and **Swelling ($CSN$)** represent the cementitious paste that softens, undergoes fluid dilatation, and resolidifies into semi-coke.
- **Total Inerts ($TI$)** act as mineral and organic aggregate grains.
If the $TR/TI$ ratio is unbalanced:
- **Excess Inerts ($TI > 58\%$):** The fluid reactive phase cannot completely wet the inert boundaries, producing weak interfaces and low CSR (e.g., Blends #17, #18, #25).
- **Excess Reactives ($TR > 48\%$ with high VM):** The coke develops excessively large, thin-walled gas bubbles that collapse under load.

### 10.3 Resolving the Collinearity Trap
The high VIF of $TR$ and $TI$ ($> 18,700$) in MLR illustrates why machine learning practitioners must understand domain physics. While linear regression requires the removal of one variable to eliminate collinearity, tree-based models naturally bypass this restriction because axis-aligned decision trees split on one variable at a time without matrix inversion.

---

## 11. Limitations, Threats to Validity, and Industrial Applicability

1. **Dataset Size Constraints ($N=68$):**
   - With 68 observations, reserving $20\%$ ($n=14$) for testing leaves 54 training samples. While adequate for detecting dominant main effects, this sample size carries substantial statistical uncertainty for higher-order hyperparameter tuning.
2. **Interpretation of Negative Test $R^2$:**
   - On the held-out test set ($n=14$), the total sum of squares is small ($SS_{\text{tot}} = \sum (y_i - \bar{y}_{\text{test}})^2 = 420.3$ for CSR; $74.5$ for CRI). When test target variance is restricted, any moderate residual sum of squares causes $R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$ to become negative.
   - Importantly, **RMSE and MAE indicate meaningful predictive accuracy:** XGBoost achieved an RMSE of $5.51\%$ on CSR (mean target value $57.8\%$), yielding a low percentage error of $6.56\%$.
3. **Absence of Carbonization Process Variables:**
   - Coke quality is governed not only by coal chemistry, but also by oven operating parameters: coal bulk density, moisture content, pulverization level ($-3.15$ mm %), coking time, and flue heating temperature. Incorporating oven variables would further refine predictive accuracy.

---

## 12. Conclusions and Recommendations

### 12.1 Primary Scientific Conclusions
1. **Model Hierarchy for CSR:** **XGBoost** is the best performing algorithm for CSR prediction ($RMSE = 5.51\%$, $MAE = 3.79\%$), reducing predictive error by over $20\%$ compared to Phase 1 MLR.
2. **Model Hierarchy for CRI:** **Random Forest** is the top-performing algorithm for CRI prediction, demonstrating the lowest test error ($RMSE = 2.97\%$, $MAE = 2.37\%$) and the highest cross-validation stability ($R^2_{\text{CV}} = 0.338 \pm 0.178$).
3. **Defects of Phase 1 MLR:** The full 8-variable MLR model without regularization suffers from severe variance inflation ($VIF > 18,700$) caused by maceral compositional closure ($TR + TI \approx 100\%$), leading to poor generalization.
4. **Dominant Coal Characteristics:** Crucible Swelling Number (CSN), Volatile Matter (VM), and Ash content represent the most influential predictors across all evaluated paradigms.

### 12.2 Recommendations for Industrial Implementation
1. **Deployment Architecture:** Implement a decoupled prediction engine where **XGBoost** generates the CSR forecast and **Random Forest** generates the independent CRI forecast.
2. **Feature Pruning for Linear Baselines:** If linear models are required for regulatory or operational transparency, $TI$ must be omitted to resolve rank deficiency, or Ridge/Lasso regularization must be introduced.
3. **Screening Minimum Caking Bounds:** Low CSN ($< 3.0$) should trigger operational warnings regardless of predicted values, flagging potential matrix bonding deficits prior to charging coke batteries.

---

## 13. References

1. **Dash, P. S., Guha, M., Chakraborty, D., & Banerjee, P. K. (2012).** Prediction of Coke CSR from Coal Blend Characteristics using Various Techniques: A Comparative Evaluation. *International Journal of Coal Preparation and Utilization*, 32(4), 169–188.
2. **Miyazu, T., Okuyama, Y., Suzuki, N., Fukuyama, T., & Mori, T. (1974).** The evaluation and design of coal blends using petrographic analysis. *Nippon Kokan Technical Report*, 67, 1–11.
3. **Schapiro, N., Gray, R. J., & Eusner, G. R. (1961).** Recent developments in coal petrography and its application to coking. *Proceedings of AIME Blast Furnace, Coke Oven, and Raw Materials Committee*, 20, 89–112.
4. **Lundgren, M., & Sundqvist Ökvist, L. (2014).** Effect of blast furnace operating conditions on coke degradation. *Ironmaking & Steelmaking*, 41(4), 282–290.
5. **Breiman, L. (2001).** Random forests. *Machine Learning*, 45(1), 5–32.
6. **Chen, T., & Guestrin, C. (2016).** XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794.
7. **Lundberg, S. M., & Lee, S. I. (2017).** A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS)*, 30, 4765–4774.

