import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure directories exist
os.makedirs('results/figures', exist_ok=True)

def load_data():
    # Use the robust loading logic we fixed earlier
    try:
        df = pd.read_csv('data/insurance_claims.csv', sep='|', low_memory=False, on_bad_lines='skip')
    except:
        df = pd.read_csv('data/insurance_claims.csv', sep=',', low_memory=False, on_bad_lines='skip')
    
    # Numeric conversion
    cols = ['TotalPremium', 'TotalClaims']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    return df

def generate_plots(df):
    print("Generating evidence plots...")
    
    # 1. LOSS RATIO BY PROVINCE
    # Loss Ratio = TotalClaims / TotalPremium
    province_stats = df.groupby('Province')[['TotalPremium', 'TotalClaims']].sum().reset_index()
    province_stats['LossRatio'] = province_stats['TotalClaims'] / province_stats['TotalPremium']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=province_stats.sort_values('LossRatio', ascending=False), x='LossRatio', y='Province', palette='viridis')
    plt.title('Loss Ratio by Province (Higher is Riskier)')
    plt.axvline(x=1.0, color='r', linestyle='--', label='Breakeven Point')
    plt.xlabel('Loss Ratio (Claims / Premium)')
    plt.tight_layout()
    plt.savefig('results/figures/loss_ratio_province.png')
    print("Saved: results/figures/loss_ratio_province.png")

    # 2. TEMPORAL TRENDS
    # Ensure TransactionMonth is datetime
    if 'TransactionMonth' in df.columns:
        df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'], errors='coerce')
        monthly_stats = df.groupby('TransactionMonth')[['TotalPremium', 'TotalClaims']].sum().reset_index()
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_stats['TransactionMonth'], monthly_stats['TotalPremium'], label='Total Premium', marker='o')
        plt.plot(monthly_stats['TransactionMonth'], monthly_stats['TotalClaims'], label='Total Claims', marker='x', color='red')
        plt.title('Temporal Trends: Premiums vs Claims (2014-2015)')
        plt.ylabel('Amount (Rand)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('results/figures/temporal_trends.png')
        print("Saved: results/figures/temporal_trends.png")

    # 3. MARGIN BY ZIPCODE (Boxplot for top zips)
    df['Margin'] = df['TotalPremium'] - df['TotalClaims']
    top_zips = df['PostalCode'].value_counts().nlargest(10).index
    zip_data = df[df['PostalCode'].isin(top_zips)]
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=zip_data, x='PostalCode', y='Margin', showfliers=False) # Hide extreme outliers for readability
    plt.title('Profit Margin Distribution by Top 10 ZipCodes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('results/figures/margin_zipcode.png')
    print("Saved: results/figures/margin_zipcode.png")

if __name__ == "__main__":
    df = load_data()
    generate_plots(df)