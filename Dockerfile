FROM apache/airflow:2.8.0-python3.9

USER root
RUN apt-get update && apt-get install -y default-jdk && apt-get clean

USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src/ /opt/airflow/src/
COPY dags/ /opt/airflow/dags/
COPY data/ /opt/airflow/input/

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PYTHONPATH="/opt/airflow"