# src/cleaning.py

def handle_missing_values(df):
    """
    Imputes missing values:
    - Numeric columns -> Median (robust to outliers)
    - Categorical columns -> Mode (most frequent)
    """
    # 1. Numerical: Fill with Median
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in num_cols:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
    
    # 2. Categorical: Fill with Mode or "Unknown"
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        mode_val = df[col].mode()[0]
        df[col] = df[col].fillna(mode_val)
        
    return df