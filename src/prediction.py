"""
Prediction Inference Module for Coke Quality Prediction Project.
Provides a standalone, reusable interface to predict CSR and CRI independently
from eight coal-blend characteristics using the best trained models.
"""

import sys
import argparse
from pathlib import Path
# pyrefly: ignore[missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
import joblib

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config


class CokeQualityPredictor:
    """
    Independent prediction engine for CSR and CRI.
    Enforces strict independence between CSR and CRI pipelines.
    """
    def __init__(self, csr_model_type="xgboost", cri_model_type="random_forest"):
        self.csr_model_type = csr_model_type
        self.cri_model_type = cri_model_type
        self.feature_cols = config.STANDARDIZED_FEATURE_COLUMNS
        self.load_models()

    def load_models(self):
        """Loads trained pipelines for CSR and CRI."""
        csr_path = config.MODELS_CSR_DIR / f"{self.csr_model_type}_model.joblib"
        cri_path = config.MODELS_CRI_DIR / f"{self.cri_model_type}_model.joblib"

        if not csr_path.exists():
            raise FileNotFoundError(f"CSR model not found at {csr_path}. Please train models first.")
        if not cri_path.exists():
            raise FileNotFoundError(f"CRI model not found at {cri_path}. Please train models first.")

        self.csr_model = joblib.load(csr_path)
        self.cri_model = joblib.load(cri_path)

    def validate_inputs(self, df_input):
        """Checks for input validity and flags extrapolations outside plausible metallurgical ranges."""
        warnings = []
        for var in self.feature_cols:
            if var not in df_input.columns:
                raise ValueError(f"Missing required feature: {var}")
            meta = config.FEATURE_METADATA.get(var, {})
            val_min = df_input[var].min()
            val_max = df_input[var].max()
            if "min" in meta and val_min < meta["min"]:
                warnings.append(f"Warning: {var} has value {val_min} < plausible metallurgical min {meta['min']}.")
            if "max" in meta and val_max > meta["max"]:
                warnings.append(f"Warning: {var} has value {val_max} > plausible metallurgical max {meta['max']}.")

        # Check TR + TI compositional sum
        if "TR" in df_input.columns and "TI" in df_input.columns:
            sum_tr_ti = df_input["TR"] + df_input["TI"]
            max_dev = np.max(np.abs(sum_tr_ti - 100.0))
            if max_dev > 1.0:
                warnings.append(f"Warning: Total Reactives (TR) + Total Inerts (TI) deviates from 100% by {max_dev:.2f}%.")

        return warnings

    def predict(self, input_data):
        """
        Accepts dictionary, DataFrame, or 2D array of 8 coal features.
        Returns DataFrame with Predicted_CSR and Predicted_CRI.
        """
        if isinstance(input_data, dict):
            # Normalize keys to standard names
            normalized = {}
            for k, v in input_data.items():
                std_k = config.COLUMN_MAPPING.get(k, k)
                normalized[std_k] = [v]
            df_in = pd.DataFrame(normalized)
        elif isinstance(input_data, pd.DataFrame):
            df_in = input_data.copy()
            # Rename if necessary
            df_in = df_in.rename(columns=config.COLUMN_MAPPING)
        elif isinstance(input_data, (list, np.ndarray)):
            df_in = pd.DataFrame(input_data, columns=self.feature_cols)
        else:
            raise TypeError("Input must be a dict, DataFrame, or numpy array.")

        # Ensure correct column ordering
        df_in = df_in[self.feature_cols]

        warnings = self.validate_inputs(df_in)

        X = df_in.values
        pred_csr = self.csr_model.predict(X)
        pred_cri = self.cri_model.predict(X)

        result_df = df_in.copy()
        result_df["Predicted_CSR (%)"] = np.round(pred_csr, 2)
        result_df["Predicted_CRI (%)"] = np.round(pred_cri, 2)

        return {
            "predictions": result_df,
            "warnings": warnings,
            "csr_model_used": self.csr_model_type,
            "cri_model_used": self.cri_model_type
        }


def main():
    parser = argparse.ArgumentParser(description="Predict Coke CSR and CRI from 8 Coal Blend Characteristics.")
    parser.add_argument("--ash", type=float, default=12.5, help="Ash content (%)")
    parser.add_argument("--vm", type=float, default=23.0, help="Volatile Matter (%)")
    parser.add_argument("--ro", type=float, default=1.12, help="Mean Vitrinite Reflectance (%)")
    parser.add_argument("--v9_v13", type=float, default=78.0, help="V9-V13 distribution (%)")
    parser.add_argument("--tr", type=float, default=45.0, help="Total Reactives (%)")
    parser.add_argument("--ti", type=float, default=55.0, help="Total Inerts (%)")
    parser.add_argument("--csn", type=float, default=3.5, help="Crucible Swelling Number")
    parser.add_argument("--bi", type=float, default=0.11, help="Basicity Index")
    parser.add_argument("--file", type=str, default=None, help="Optional CSV file path for batch prediction")

    args = parser.parse_args()

    predictor = CokeQualityPredictor(csr_model_type="xgboost", cri_model_type="random_forest")

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist.")
            sys.exit(1)
        df_batch = pd.read_csv(file_path)
        out = predictor.predict(df_batch)
        print("\n=== Batch Prediction Results ===")
        print(out["predictions"][["Predicted_CSR (%)", "Predicted_CRI (%)"]])
        out_path = config.PREDICTIONS_DIR / "batch_predictions_output.csv"
        out["predictions"].to_csv(out_path, index=False)
        print(f"Saved full predictions to: {out_path}")
    else:
        sample_input = {
            "Ash": args.ash,
            "VM": args.vm,
            "Ro": args.ro,
            "V9_V13": args.v9_v13,
            "TR": args.tr,
            "TI": args.ti,
            "CSN": args.csn,
            "BI": args.bi
        }
        out = predictor.predict(sample_input)
        print("\n=== Single Blend Prediction Results ===")
        print(f"Inputs: {sample_input}")
        print(f"CSR Model: {out['csr_model_used'].upper()} -> Predicted CSR: {out['predictions']['Predicted_CSR (%)'].iloc[0]} %")
        print(f"CRI Model: {out['cri_model_used'].upper()} -> Predicted CRI: {out['predictions']['Predicted_CRI (%)'].iloc[0]} %")
        if out["warnings"]:
            print("\nWarnings:")
            for w in out["warnings"]:
                print(" -", w)


if __name__ == "__main__":
    main()

