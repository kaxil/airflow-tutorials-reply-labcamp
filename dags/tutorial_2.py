# Import builtin module
import datetime as dt

# Import Airflow modules
from airflow import DAG
from airflow.models import Variable
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(year=2018, month=10, day=20)
}

dag = DAG(
    dag_id='airflow_tutorial_2_v01',
    default_args=default_args,
    schedule_interval=None,
)

print_hello = BashOperator(
    task_id='print_hello',
    bash_command='echo "Hello"',
    dag=dag
)

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath=Variable.get("success_file_path"),
    # filepath='Users/kaxil/Desktop/_success',
    fs_conn_id='localhost_files',
    dag=dag
)

print_world = BashOperator(
    task_id='print_world',
    bash_command='echo "World. File Received."',
    dag=dag
)

etl = DummyOperator(
    task_id='etl',
    dag=dag
)

print_hello >> file_sensor >> print_world >> etl
