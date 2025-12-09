import seaborn as sns
import matplotlib.pyplot as plt

def plot_outliers(df, column_name):
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=df[column_name])
    plt.title(f'Outlier Detection: {column_name}')
    plt.xlabel(column_name)
    plt.show()

# Usage:
# plot_outliers(df, 'TotalPremium')
# plot_outliers(df, 'TotalClaims')