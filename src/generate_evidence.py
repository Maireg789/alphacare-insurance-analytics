import pandas as pd
import os

def print_evidence():
    # 1. Try to find the data file. 
    # AlphaCare data is usually named 'MachineLearningRating_v3.txt'
    file_path = "data/MachineLearningRating_v3.txt"
    
    # If that specific file doesn't exist, check for a CSV
    if not os.path.exists(file_path):
        file_path = "data/insurance_claims.csv"
        
    if not os.path.exists(file_path):
        print("❌ ERROR: Could not find data file.")
        print("Please check your 'data' folder and update the 'file_path' variable in this script.")
        return

    print(f"✅ Loading data from: {file_path} ...\n")
    
    # Load data (handling the pipe '|' separator common in this project)
    try:
        df = pd.read_csv(file_path, sep='|', low_memory=False)
    except:
        # Fallback to standard comma separator if pipe fails
        df = pd.read_csv(file_path, low_memory=False)

    # EVIDENCE 1: Missing Values
    print("=== COPY THIS FOR TABLE 1 (Missing Values) ===")
    print(df.isnull().sum()[df.isnull().sum() > 0]) # Only show columns with missing data
    print("==============================================\n")

    # EVIDENCE 2: Descriptive Statistics
    print("=== COPY THIS FOR TABLE 2 (Stats) ===")
    # specific columns relevant to the project
    cols = ['TotalPremium', 'TotalClaims'] 
    if all(col in df.columns for col in cols):
        print(df[cols].describe().to_string())
    else:
        print(df.describe().to_string())
    print("=========================================\n")

if __name__ == "__main__":
    print_evidence()