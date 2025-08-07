import os

class Config:
    INPUT_CSV_PATH: str = "/opt/airflow/input/sales-orders.csv"  
    
    DATA_DIR: str = os.getenv("DATA_DIR", "/opt/airflow/data") 
    RAW_DATA_DIR: str = f"{DATA_DIR}/raw"
    PROCESSED_DATA_DIR: str = f"{DATA_DIR}/processed"
    
    RAW_PARQUET_PATH: str = f"{RAW_DATA_DIR}/sales-orders.parquet"
    PROCESSED_PARQUET_PATH: str = f"{PROCESSED_DATA_DIR}/top_products.parquet"
    
    MINIO_HOST: str = os.getenv("MINIO_HOST", "mini-etl-minio-service:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "sales-data")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    
    SPARK_APP_NAME: str = "MiniETLPipeline"
    TOP_PRODUCTS_LIMIT: int = 10