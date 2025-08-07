import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from ..config import Config

class Transformer:    
    def __init__(self, config: Config = Config()):
        self.config = config
        self.spark = None
    
    def _create_spark_session(self) -> SparkSession:
        return SparkSession.builder \
            .appName(self.config.SPARK_APP_NAME) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.driver.memory", "512m") \
            .config("spark.executor.memory", "512m") \
            .config("spark.driver.maxResultSize", "256m") \
            .config("spark.sql.shuffle.partitions", "4") \
            .getOrCreate()
    
    def transform_sales_data(self) -> None:
        try:
            self.spark = self._create_spark_session()
            os.makedirs(os.path.dirname(self.config.PROCESSED_PARQUET_PATH), exist_ok=True)
            
            df = self.spark.read.parquet(self.config.RAW_PARQUET_PATH)
            
            if "Item Type" in df.columns:
                df_renamed = df.withColumnRenamed("Item Type", "product_name") \
                              .withColumnRenamed("Units Sold", "quantity") \
                              .withColumnRenamed("Unit Price", "unit_price")
            else:
                df_renamed = df
            
            df_with_revenue = df_renamed.withColumn("Total_Revenue", col("quantity") * col("unit_price"))
            
            top_products = df_with_revenue.groupBy("product_name") \
                .agg(spark_sum("Total_Revenue").alias("Total_Revenue")) \
                .orderBy(col("Total_Revenue").desc()) \
                .limit(self.config.TOP_PRODUCTS_LIMIT)
            
            top_products.write.mode("overwrite").parquet(self.config.PROCESSED_PARQUET_PATH)
            
            print(f"Top {self.config.TOP_PRODUCTS_LIMIT} products by revenue:")
            top_products.show()
            print(f"Results saved to: {self.config.PROCESSED_PARQUET_PATH}")
            
        except Exception as e:
            print(f"Error during transformation: {e}")
            raise e
        finally:
            if self.spark:
                self.spark.stop()

def transform() -> None:
    transformer = Transformer()
    transformer.transform_sales_data()

if __name__ == "__main__":
    transform()