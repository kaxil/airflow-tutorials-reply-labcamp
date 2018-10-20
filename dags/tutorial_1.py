# Import builtin module
import datetime as dt

# Import Airflow modules
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def print_world():
    print('world')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # 'start_date': airflow.utils.dates.days_ago(2),
    # You can also set the start date as follows
    'start_date': dt.datetime(year=2018, month=10, day=22),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='airflow_tutorial_v01',
    default_args=default_args,
    schedule_interval='0 * * * *',
    # You can also specify schedule interval as follows
    # schedule_interval=dt.timedelta(hours=1)
)

print_hello = BashOperator(
    task_id='print_hello',
    bash_command='echo "hello"',
    dag=dag
)

sleep = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    dag=dag
)

print_world = PythonOperator(
    task_id='print_world',
    python_callable=print_world,
    dag=dag
)


# one way of setting dependencies
print_hello >> sleep >> print_world

# other way of setting dependencies
# sleep.set_upstream(print_hello) # Equivalent to print_hello.set_downstream(sleep)
# print_world.set_upstream(sleep) # Equivalent to sleep.set_downstream(print_world)
