import pandas as pd
import os
from src.utils import get_logger

logger = get_logger('DataLoader')

class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Loads data and validates columns."""
        if not os.path.exists(self.filepath):
            logger.error(f"File not found: {self.filepath}")
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        try:
            # Using pipe separator '|'
            self.df = pd.read_csv(self.filepath, sep='|', low_memory=False)
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            
            # Validation Step
            self._validate_columns()
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise e
        
        return self.df

    def _validate_columns(self):
        """Ensures critical columns for analysis exist."""
        required_cols = ['TotalPremium', 'TotalClaims', 'Province', 'PostalCode']
        missing = [col for col in required_cols if col not in self.df.columns]
        
        if missing:
            logger.warning(f"⚠️ Missing critical columns: {missing}")
        else:
            logger.info("✅ All critical columns are present.")