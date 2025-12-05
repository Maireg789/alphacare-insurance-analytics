import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class EDAStrategy:
    """
    Class responsible for Exploratory Data Analysis and Visualization.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Set a professional plotting style
        sns.set_theme(style="whitegrid")

    def describe_financials(self):
        """Descriptive stats for key financial columns."""
        cols = ['TotalPremium', 'TotalClaims']
        print("\n📊 --- Financial Descriptive Stats ---")
        print(self.df[cols].describe())

    def plot_distributions(self):
        """Univariate Analysis: Histograms for Premium and Claims."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # TotalPremium Distribution (Log scale to handle skew)
        sns.histplot(self.df['TotalPremium'], bins=50, ax=axes[0], color='blue')
        axes[0].set_title('Distribution of Total Premium')
        axes[0].set_yscale('log') # Log scale helps view skewed insurance data

        # TotalClaims Distribution
        sns.histplot(self.df['TotalClaims'], bins=50, ax=axes[1], color='red')
        axes[1].set_title('Distribution of Total Claims')
        axes[1].set_yscale('log')

        plt.tight_layout()
        plt.show()

    def plot_claims_by_category(self, category_col: str):
        """Bivariate Analysis: Claims per Category (e.g., Province)."""
        plt.figure(figsize=(12, 6))
        # Group by category and sum claims
        data = self.df.groupby(category_col)['TotalClaims'].sum().sort_values(ascending=False).reset_index()
        
        sns.barplot(x=category_col, y='TotalClaims', data=data, palette='viridis')
        plt.title(f'Total Claims by {category_col}')
        plt.xticks(rotation=45)
        plt.ylabel('Total Claims (Currency)')
        plt.show()

    def detect_outliers(self):
        """Outlier Detection using Boxplots."""
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=self.df['TotalClaims'])
        plt.title('Boxplot for Total Claims (Outlier Detection)')
        plt.show()