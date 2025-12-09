import pandas as pd
import scipy.stats as stats
import os
import sys

def load_data(filepath):
    """
    Loads data by forcing the delimiter to '|' (pipe), which is standard 
    for this dataset, or falling back to ',' (comma).
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        sys.exit(1)

    print(f"Attempting to load {filepath}...")

    # Method 1: Try Pipe '|' Separator (Most likely correct)
    try:
        print("   [System] Trying pipe '|' delimiter...")
        # Reading 500k rows to be safe on memory
        df = pd.read_csv(filepath, sep='|', nrows=500000, on_bad_lines='skip', low_memory=False)
        
        # Check if it actually worked by looking for the target column
        # We strip whitespace from columns just in case
        df.columns = df.columns.str.strip()
        
        if 'TotalClaims' in df.columns:
            print(f"   [Success] Loaded with pipe '|'. Shape: {df.shape}")
            return df
        else:
            print("   [Warning] Pipe delimiter loaded data, but 'TotalClaims' column is missing.")
            print(f"   Columns found: {list(df.columns[:5])}...")
            # If pipe failed to find the right columns, we might try comma
            raise ValueError("Columns missing with pipe delimiter")

    except Exception as e:
        print(f"   [System] Pipe failed ({e}). Trying comma ',' delimiter...")

    # Method 2: Fallback to Comma ',' Separator
    try:
        df = pd.read_csv(filepath, sep=',', nrows=500000, on_bad_lines='skip', low_memory=False)
        df.columns = df.columns.str.strip()
        print(f"   [Success] Loaded with comma ','. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"   [Critical Error] Could not load data. {e}")
        sys.exit(1)

def perform_hypothesis_testing(df):
    print("\n==================================================")
    print("           TASK 3: HYPOTHESIS TESTING             ")
    print("==================================================")

    # --- DIAGNOSTIC: Print Columns ---
    # This helps you debug if the columns are named slightly differently
    print(f"Columns in dataset: {list(df.columns)}")

    # --- DATA PREPARATION ---
    # Convert financial columns to numeric (coerce errors to NaN, then fill 0)
    cols_to_numeric = ['TotalPremium', 'TotalClaims']
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            print(f"Error: Required column '{col}' is missing!")
            return

    # Create Features
    df['Claim_Flag'] = df['TotalClaims'].apply(lambda x: 1 if x > 0 else 0)
    df['Margin'] = df['TotalPremium'] - df['TotalClaims']

    # --- TEST 1: Risk Differences Across Provinces ---
    if 'Province' in df.columns:
        print("\n[Test 1] Risk (Frequency) across Provinces")
        contingency = pd.crosstab(df['Province'], df['Claim_Flag'])
        chi2, p, dof, ex = stats.chi2_contingency(contingency)
        print(f"   Chi2 Stat: {chi2:.2f}, P-value: {p:.4e}")
        interpret_p_value(p)
    else:
        print("\n[Test 1] Skipped: 'Province' column not found.")

    # --- TEST 2: Risk Differences Between ZipCodes ---
    if 'PostalCode' in df.columns:
        print("\n[Test 2] Risk (Frequency) across ZipCodes")
        top_zips = df['PostalCode'].value_counts().nlargest(20).index
        zip_df = df[df['PostalCode'].isin(top_zips)]
        
        contingency_zip = pd.crosstab(zip_df['PostalCode'], zip_df['Claim_Flag'])
        chi2, p, dof, ex = stats.chi2_contingency(contingency_zip)
        print(f"   Chi2 Stat: {chi2:.2f}, P-value: {p:.4e} (Top 20 Zips)")
        interpret_p_value(p)
    else:
        print("\n[Test 2] Skipped: 'PostalCode' column not found.")

    # --- TEST 3: Margin Difference Between ZipCodes ---
    if 'PostalCode' in df.columns:
        print("\n[Test 3] Margin (Profit) Difference across ZipCodes")
        top_zips = df['PostalCode'].value_counts().nlargest(20).index
        zip_df = df[df['PostalCode'].isin(top_zips)]
        
        groups = [data['Margin'].values for name, data in zip_df.groupby('PostalCode')]
        
        if len(groups) > 1:
            f_stat, p = stats.f_oneway(*groups)
            print(f"   F-Stat: {f_stat:.2f}, P-value: {p:.4e}")
            interpret_p_value(p)
        else:
            print("   Not enough groups for ANOVA.")

    # --- TEST 4: Risk Difference Between Women and Men ---
    if 'Gender' in df.columns:
        print("\n[Test 4] Risk (Frequency) Women vs Men")
        df['Gender_Clean'] = df['Gender'].astype(str).str.lower().str.strip()
        gender_df = df[df['Gender_Clean'].isin(['male', 'female', 'm', 'f'])]
        
        if not gender_df.empty:
            contingency_gender = pd.crosstab(gender_df['Gender_Clean'], gender_df['Claim_Flag'])
            chi2, p, dof, ex = stats.chi2_contingency(contingency_gender)
            print(f"   Chi2 Stat: {chi2:.2f}, P-value: {p:.4e}")
            interpret_p_value(p)
        else:
            print("   No standard 'Male'/'Female' data found.")
    else:
        print("\n[Test 4] Skipped: 'Gender' column not found.")

def interpret_p_value(p):
    if p < 0.05:
        print("   Result: REJECT Null Hypothesis (Significant difference).")
    else:
        print("   Result: FAIL TO REJECT Null Hypothesis (No difference).")

if __name__ == "__main__":
    data_path = "data/insurance_claims.csv" 
    df = load_data(data_path)
    if df is not None:
        perform_hypothesis_testing(df)