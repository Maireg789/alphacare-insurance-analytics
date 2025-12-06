import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import get_logger

logger = get_logger('EDA')

class EDAStrategy:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        sns.set_theme(style="whitegrid")

    def plot_distributions(self):
        """Univariate: Histograms."""
        logger.info("Generating distribution plots...")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Log scale handles the massive difference between 0 and high claims
        if 'TotalPremium' in self.df.columns:
            sns.histplot(self.df['TotalPremium'], bins=50, ax=axes[0], color='teal', log_scale=(False, True))
            axes[0].set_title('Total Premium Distribution (Log Scale)')
        
        if 'TotalClaims' in self.df.columns:
            sns.histplot(self.df['TotalClaims'], bins=50, ax=axes[1], color='coral', log_scale=(False, True))
            axes[1].set_title('Total Claims Distribution (Log Scale)')
        
        plt.tight_layout()
        plt.show()

    def plot_correlations(self):
        """
        Multivariate: Correlation Matrix.
        Identifies relationships between numerical financial variables.
        """
        logger.info("Generating correlation matrix...")
        # Select only numeric columns
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        
        # Focus on key financial fields to avoid noise
        key_cols = ['TotalPremium', 'TotalClaims', 'CalculatedPremiumPerTerm', 'SumInsured']
        
        # Check which columns actually exist in the data
        valid_cols = [col for col in key_cols if col in numeric_df.columns]
        
        if len(valid_cols) > 1:
            subset_df = numeric_df[valid_cols]
            plt.figure(figsize=(10, 8))
            corr = subset_df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
            plt.title('Multivariate Analysis: Financial Correlation Matrix')
            plt.show()
        else:
            logger.warning("Not enough numeric columns found for correlation matrix.")

    def plot_scatter_premium_vs_claims(self):
        """
        Multivariate: Scatter Plot.
        Tests the hypothesis: Do higher premiums actually correlate with higher claims?
        """
        logger.info("Generating Premium vs Claims scatter plot...")
        
        if 'TotalPremium' in self.df.columns and 'TotalClaims' in self.df.columns:
            plt.figure(figsize=(10, 6))
            
            # Sampling 5000 points to keep the plot readable and fast
            sample_df = self.df.sample(n=min(5000, len(self.df)), random_state=42)
            
            # Check if Province exists for coloring, otherwise ignore hue
            hue_col = 'Province' if 'Province' in self.df.columns else None
            
            sns.scatterplot(data=sample_df, x='TotalPremium', y='TotalClaims', hue=hue_col, alpha=0.6)
            plt.title('Total Premium vs. Total Claims (Sampled 5k points)')
            plt.show()
        else:
            logger.warning("TotalPremium or TotalClaims columns missing, skipping scatter plot.")