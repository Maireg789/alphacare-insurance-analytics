import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import shap
import os
import sys

# Ensure results directory exists
os.makedirs('results/figures', exist_ok=True)

def load_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        sys.exit(1)
    
    print(f"Loading data from {filepath}...")
    # Use pipe separator
    df = pd.read_csv(filepath, sep='|', low_memory=False, on_bad_lines='skip')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Force financial columns to numeric
    cols_to_numeric = ['TotalPremium', 'TotalClaims', 'CalculatedPremiumPerTerm', 'SumInsured']
    for col in cols_to_numeric:
        if col in df.columns:
            # Coerce errors turns non-numeric text to NaN, then we fill with 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

def train_models(df):
    print("\n==================================================")
    print("           TASK 4: PREDICTIVE MODELING            ")
    print("==================================================")

    # --- 1. DATA PREPARATION ---
    # Filter for rows with actual claims
    modeling_df = df[df['TotalClaims'] > 0].copy()
    print(f"Training on {len(modeling_df)} rows where TotalClaims > 0")

    # --- CORRECTION: Explicit Feature Lists ---
    # We explicitly define lists here to prevent any "Monthly" strings entering numeric processors
    numeric_features = ['CalculatedPremiumPerTerm', 'SumInsured']
    categorical_features = ['Province', 'VehicleType', 'Bodytype', 'Gender', 'TermFrequency']
    
    # Debug Print to confirm lists are correct
    print(f"Numeric Features: {numeric_features}")
    print(f"Categorical Features: {categorical_features}")

    # Check which columns actually exist in the data
    available_numeric = [c for c in numeric_features if c in modeling_df.columns]
    available_categorical = [c for c in categorical_features if c in modeling_df.columns]
    
    # Force Categorical columns to String type to avoid type errors
    for col in available_categorical:
        modeling_df[col] = modeling_df[col].astype(str)

    # Drop rows with missing values in these columns
    modeling_df = modeling_df.dropna(subset=available_numeric + available_categorical)
    
    X = modeling_df[available_numeric + available_categorical]
    y = modeling_df['TotalClaims']

    # --- 2. PIPELINE SETUP ---
    # Scale numbers, One-Hot encode categories
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, available_numeric),
            ('cat', categorical_transformer, available_categorical)
        ])

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 3. DEFINE MODELS ---
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
        "XGBoost": XGBRegressor(n_estimators=50, learning_rate=0.1, random_state=42, n_jobs=-1)
    }

    best_model = None
    best_score = -float("inf")
    best_name = ""

    # --- 4. TRAIN & EVALUATE ---
    for name, model in models.items():
        print(f"\nTraining {name}...")
        try:
            pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                       ('model', model)])
            
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"   -> RMSE: {rmse:,.2f}")
            print(f"   -> MAE:  {mae:,.2f}")
            print(f"   -> R2:   {r2:.4f}")
            
            if r2 > best_score:
                best_score = r2
                best_model = pipeline
                best_name = name
        except Exception as e:
            print(f"   [Error] Failed to train {name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n[Winner] Best Model: {best_name} (R2: {best_score:.4f})")

    # --- 5. FEATURE IMPORTANCE (SHAP) ---
    if best_name in ["Random Forest", "XGBoost"]:
        print("\nGenerating SHAP Feature Importance Plot...")
        
        try:
            model_step = best_model.named_steps['model']
            preprocessor_step = best_model.named_steps['preprocessor']
            
            X_test_transformed = preprocessor_step.transform(X_test)
            
            cat_names = preprocessor_step.named_transformers_['cat'].get_feature_names_out(available_categorical)
            feature_names = available_numeric + list(cat_names)
            
            # Using a small sample for SHAP to speed up processing
            explainer = shap.Explainer(model_step, X_test_transformed)
            shap_values = explainer(X_test_transformed[:500]) 
            
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, X_test_transformed[:500], feature_names=feature_names, show=False)
            output_path = 'results/figures/shap_summary.png'
            plt.savefig(output_path, bbox_inches='tight')
            print(f"   -> Plot saved to {output_path}")
            
        except Exception as e:
            print(f"   [Warning] Could not generate SHAP plot: {e}")

if __name__ == "__main__":
    data_path = "data/insurance_claims.csv" 
    df = load_data(data_path)
    train_models(df)