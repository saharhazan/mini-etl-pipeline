import os
import pandas as pd
from ..config import Config

class Extractor:
    def __init__(self, config: Config = Config()):
        self.config = config
    
    def extract_csv_to_parquet(self) -> None:
        os.makedirs(os.path.dirname(self.config.RAW_PARQUET_PATH), exist_ok=True)
        df = pd.read_csv(self.config.INPUT_CSV_PATH)
        df.to_parquet(self.config.RAW_PARQUET_PATH, index=False)
        print(f"Successfully extracted {len(df)} records from CSV to Parquet")
        print(f"Output saved to: {self.config.RAW_PARQUET_PATH}")

def extract() -> None:
    extractor = Extractor()
    extractor.extract_csv_to_parquet()

if __name__ == "__main__":
    extract()