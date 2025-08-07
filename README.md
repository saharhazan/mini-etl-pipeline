# Mini ETL Pipeline

A simple ETL pipeline that processes sales data using Apache Airflow on Kubernetes.

## Overview

This project implements an ETL pipeline that:
- Extracts sales data from CSV files
- Transforms data using PySpark to calculate top product categories
- Loads results into MinIO object storage

## Technology Stack

- Apache Airflow - Workflow orchestration
- PySpark - Data processing
- MinIO - Object storage
- PostgreSQL - Airflow metadata database
- Kubernetes - Container orchestration
- Docker - Containerization

## Project Structure

```
├── README.md
├── Dockerfile
├── requirements.txt
├── dags/
│   └── mini_etl_dag.py
├── src/etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── data/
│   └── sales-orders.csv
└── helm/mini-etl/
```

## Requirements

- Docker Desktop
- Minikube
- Helm 3.x
- kubectl
- 4GB+ RAM for Minikube

## Setup Instructions

### 1. Start Minikube

```bash
minikube start --memory=4096 --cpus=2
```

### 2. Build Docker Image

```bash
eval $(minikube docker-env)
docker build -t saharhazan/etl-airflow:latest .
```

### 3. Deploy with Helm

Set the project path and deploy:

```bash
export PROJECT_PATH=$(pwd)
helm install mini-etl-airflow helm/mini-etl \
  --set projectPath="$PROJECT_PATH" \
  --namespace airflow --create-namespace
kubectl get pods -n airflow -w
```

### 4. Access Services

Get Minikube IP:
```bash
minikube ip
```

Access URLs:
- Airflow: http://MINIKUBE_IP:31151 (admin/admin)
- MinIO: http://MINIKUBE_IP:31091 (minioadmin/minioadmin)

## Running the Pipeline

1. Open Airflow web interface
2. Find the mini_etl_pipeline DAG
3. Toggle the DAG to ON
4. Click the trigger button to start execution
5. Monitor progress in the Graph View
6. Check results in MinIO console

## Pipeline Details

The pipeline consists of three sequential tasks:

1. extract_csv_to_parquet - Converts CSV data to Parquet format
2. transform_calculate_top_products - Calculates top categories using PySpark
3. load_to_minio - Uploads processed data to MinIO storage

## Output

Results are stored in MinIO under the etl-data bucket:

```
etl-data/
├── raw/
│   └── sales-orders.parquet
└── processed/
    └── top_products.parquet
```

## Troubleshooting

Common issues and solutions:

**Pods not starting:**
```bash
kubectl describe pod POD_NAME -n airflow
```

**Memory issues:**
```bash
minikube delete
minikube start --memory=6144 --cpus=3
```

**Cannot access services:**
```bash
minikube service airflow-service --namespace airflow
kubectl port-forward -n airflow service/minio-service 9001:9001
```

**Image not found error:**
Ensure you ran `eval $(minikube docker-env)` before building the Docker image.

## Cleanup

```bash
helm uninstall mini-etl-airflow --namespace airflow
minikube stop
```

---

## Author

**Sahar Hazan**