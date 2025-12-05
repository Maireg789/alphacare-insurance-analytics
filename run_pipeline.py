from src.loader import DataLoader
from src.eda import EDAStrategy
from src.utils import get_logger

logger = get_logger('MainPipeline')

if __name__ == "__main__":
    logger.info("Starting AlphaCare Analysis Pipeline...")

    # 1. Load Data
    loader = DataLoader('data/insurance_claims.csv')
    df = loader.load_data()

    # 2. Run EDA
    if df is not None:
        eda = EDAStrategy(df)
        
        # Univariate
        eda.plot_distributions()
        
        # Multivariate (Correlation) - Fills the gap in feedback
        eda.plot_correlations()
        eda.plot_scatter_premium_vs_claims()
        
    logger.info("Pipeline completed successfully.")