from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

# Define default arguments for the DAGs
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 2),
    'retries': 1,
}

dag = DAG(
    'immo-eliza',
    default_args=default_args,
    description='DockerOperator DAGs for Immo Eliza',
    schedule_interval='@daily',
)

train_model_task = DockerOperator(
    task_id='train_model_task',
    image='ml-model:latest',  
    api_version='auto', 
    auto_remove=False,  
    command='python train.py', 
    dag=dag,
)

run_api_task = DockerOperator(
    task_id='run_api_task',
    image='api:latest',  
    api_version='auto', 
    auto_remove=False,  
    command='uvicorn app:app --reload',   
    dag=dag,
)

run_streamlit_task = DockerOperator(
    task_id='run_streamlit_task',
    image='streamlit_app:latest',  
    api_version='auto', 
    auto_remove=False,  
    command='streamlit run streamlit_app.py', 
    dag=dag,
)

# Set the task dependency between the two DAGs
train_model_task >> run_api_task >> run_streamlit_task
