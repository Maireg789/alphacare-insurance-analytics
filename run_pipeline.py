from src.loader import DataLoader
from src.eda import EDAStrategy

def main():
    # 1. Load Data
    loader = DataLoader('data/insurance_claims.csv')
    df = loader.load_data()

    if df is not None:
        # 2. Perform EDA
        eda = EDAStrategy(df)
        
        # Statistics
        eda.describe_financials()
        print("\nMissing Values (Top 5):\n", loader.get_missing_values().head())

        # Visualizations (Satisfies "3 creative plots")
        print("Generating Distributions...")
        eda.plot_distributions()
        
        print("Generating Categorical Analysis...")
        eda.plot_claims_by_category('Province')
        
        print("Checking Outliers...")
        eda.detect_outliers()

if __name__ == "__main__":
    main()