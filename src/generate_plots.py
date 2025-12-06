import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the figures directory exists
os.makedirs("results/figures", exist_ok=True)

def plot_box_outliers(df, column, filename):
    """
    Generates a box plot to visualize outliers and saves it to a file.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Outlier Analysis: {column}')
    plt.xlabel(column)
    
    # Save the figure instead of showing it
    save_path = f"results/figures/{filename}"
    plt.savefig(save_path)
    print(f"Figure saved: {save_path}")
    plt.close()

if __name__ == "__main__":
    # Load your data (adjust the path to match your project)
    # Example: df = pd.read_csv("data/processed_data.csv")
    
    # FOR TESTING (Remove this and load your real CSV)
    data = {'TotalPremium': [100, 200, 150, 120, 5000, 100], 
            'TotalClaims': [0, 50, 20, 0, 10000, 0]} 
    df = pd.DataFrame(data)

    # Generate the requested plots
    plot_box_outliers(df, 'TotalPremium', 'boxplot_premium.png')
    plot_box_outliers(df, 'TotalClaims', 'boxplot_claims.png')