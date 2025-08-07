# Uploads processed Parquet files from local storage to MinIO object storage
import os
from minio import Minio
from ..config import Config

class Loader:
    def __init__(self, config: Config = Config()):
        self.config = config
        self.client = None
    
    def _create_minio_client(self) -> Minio:
        return Minio(
            self.config.MINIO_HOST,
            access_key=self.config.MINIO_ACCESS_KEY,
            secret_key=self.config.MINIO_SECRET_KEY,
            secure=self.config.MINIO_SECURE
        )
    
    def load_to_minio(self) -> None:
        self.client = self._create_minio_client()
        
        if not self.client.bucket_exists(self.config.MINIO_BUCKET):
            self.client.make_bucket(self.config.MINIO_BUCKET)
        
        uploaded_files = 0
        for root, dirs, files in os.walk(self.config.PROCESSED_PARQUET_PATH):
            for file in files:
                if file.endswith('.parquet'):
                    local_path = os.path.join(root, file)
                    object_name = f"processed/{file}"
                    self.client.fput_object(self.config.MINIO_BUCKET, object_name, local_path)
                    uploaded_files += 1
        
        print(f"Uploaded {uploaded_files} files to MinIO")

def load() -> None:
    loader = Loader()
    loader.load_to_minio()

if __name__ == "__main__":
    load()