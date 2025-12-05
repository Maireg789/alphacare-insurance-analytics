import pandas as pd
import os

class DataLoader:
    """
    Class responsible for loading and basic cleaning of insurance data.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Loads data from CSV handling pipe separators."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found at: {self.filepath}")
        
        try:
            # The data uses '|' as a separator based on previous analysis
            self.df = pd.read_csv(self.filepath, sep='|', low_memory=False)
            print(f"✅ Data Loaded Successfully. Shape: {self.df.shape}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
        
        return self.df

    def get_missing_values(self):
        """Returns the count of missing values per column."""
        return self.df.isnull().sum()