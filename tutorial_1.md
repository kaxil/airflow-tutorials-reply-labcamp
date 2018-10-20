# Tutorial 1

**Goal**: Getting familiar with building, scheduling and running your first workflow (DAG).  
**Time**: 30 minutes  
**Objectives**: 
* Running Airflow Webserver and Scheduler
* Write your first DAG
* Changing your Schedule Interval and other exercises

### Run Airflow
Before you can use Airflow you have to initialize its database.
The database contains information about historical & running workflows, connections to external data sources, 
user management, etc.
Once the database is set up, Airflow's UI can be accessed by running a web server and workflows can be started.

The default database is a SQLite database, which is fine for this tutorial.
In a production setting you'll probably be using something like MySQL or PostgreSQL.
You'll probably want to back it up as this database stores the state of everything related to Airflow.

Airflow will use the directory set in the environment variable `AIRFLOW_HOME` to store its configuration and our SQlite database.
This directory will be used after your first Airflow command.
If you don't set the environment variable `AIRFLOW_HOME`, Airflow will create the directory `~/airflow/` to put its files in.

Set environment variable `AIRFLOW_HOME`:

```bash
export AIRFLOW_HOME=~/airflow
```

or any other suitable directory.

Next, initialize the database:

```bash
airflow initdb
```

Now start the web server and go to [localhost:8080](http://localhost:8080/) to check out the UI:

```bash
airflow webserver --port 8080
```
Start the Scheduler in a different terminal session:

```bash
airflow scheduler
```

### Workflows

We'll create a workflow by specifying actions as a Directed Acyclic Graph (DAG) in Python.
The tasks of a workflow make up a Graph; the graph is Directed because the tasks are ordered; and we don't want to get stuck in an eternal loop so the graph also has to be Acyclic.

The figure below shows an example of a DAG:

<img src="https://airflow.incubator.apache.org/_images/subdag_before.png" style="width: 70%;"/>

The DAG of this tutorial is a bit easier.
It will consist of the following tasks:

* print `'hello'`
* wait 5 seconds
* print `'world` 

and we'll plan daily execution of this workflow.


### Create a DAG file

Go to the folder that you've designated to be your `AIRFLOW_HOME` and find the DAGs folder located in subfolder `dags/` (if you cannot find, create one).
Create a Python file with the name `tutorial_1.py` that will contain your DAG.
Your workflow will automatically be picked up and scheduled to run.

First we'll configure settings that are shared by all our tasks.
Settings for tasks can be passed as arguments when creating them, but we can also pass a dictionary with default values to the DAG.
This allows us to share default arguments for all the tasks in our DAG is the best place to set e.g. the owner and start date of our DAG.

Add the following import and dictionary to `tutorial_1.py` to specify the owner, start time, and retry settings that are shared by our tasks:


### Configure common settings

```python
import datetime as dt

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 10, 22),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}
```

These settings tell Airflow that this workflow is owned by `'airflow'`, that the workflow is valid since October 22nd of 2018, it should not send emails and it is allowed to retry the workflow once if it fails with a delay of 5 minutes.
Other common default arguments are email settings on failure and the end time.


### Create the DAG

We'll now create a DAG object that will contain our tasks.

Name it `airflow_tutorial_v01` and pass `default_args`:

```python
from airflow import DAG

dag = DAG(
    dag_id='airflow_tutorial_v01',
    default_args=default_args,
    schedule_interval='0 * * * *',
    # You can also specify schedule interval as follows
    # schedule_interval=dt.timedelta(hours=1)
)
```

With `schedule_interval='0 * * * *'` we've specified a run every hour; the DAG will run each hour at 00 mins 00 secs.
See [crontab.guru](https://crontab.guru/#0_*_*_*_*) for help deciphering cron schedule expressions.
Alternatively, you can use strings like `'@daily'` and `'@hourly'`.

Airflow will generate DAG runs from the `start_date` with the specified `schedule_interval`.
Once a DAG is active, Airflow continuously checks in the database if all the DAG runs have successfully ran since the `start_date`.
Any missing DAG runs are automatically scheduled.
When you initialize on 2018-10-24 a DAG with a `start_date` at 2018-10-22 and a daily `schedule_interval`, Airflow will schedule DAG runs for all the days between 2018-10-22 and 2018-10-24.

A run starts _after_ the time for the run has passed.
The time for which the workflow runs is called the `execution_date`.
The daily workflow for 2018-10-23 runs after 2018-10-23 23:59 and the hourly workflow for 2018-10-23 01:00 starts after 2018-10-23 01:59.

From the ETL viewpoint this makes sense: you can only process the daily data for a day after it has passed.

Because Airflow saves all the (scheduled) DAG runs in its database, you should not change the `start_date` and `schedule_interval` of a DAG.
Instead, up the version number of the DAG (e.g. `airflow_tutorial_v02`) and avoid running unnecessary tasks by using the web interface or command line tools

Timezones and especially daylight savings can mean trouble when scheduling things, so keep your Airflow machine in UTC.
You don't want to skip an hour because daylight savings kicks in (or out).


### Create the tasks

Tasks are represented by operators that either perform an action, transfer data, or sense if something has been done.
Examples of actions are running a bash script or calling a Python function; of transfers are copying tables between databases or uploading a file; and of sensors are checking if a file exists or data has been added to a database.

We'll create a workflow consisting of three tasks: we'll print 'hello', wait for 10 seconds and finally print 'world'. 
The first two are done with the `BashOperator` and the latter with the `PythonOperator`.
Give each operator an unique task ID and something to do:

```python
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def print_world():
    print('world')

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

```

Note how we can pass bash commands in the `BashOperator` and that the `PythonOperator` asks for a Python function that can be called.

Dependencies in tasks are added by setting other actions as upstream (or downstream). 
Link the operations in a chain so that `sleep` will be run after `print_hello` and is followed by `print_world`; `print_hello` -> `sleep` -> `print_world`:

```python
print_hello >> sleep >> print_world
```

After rearranging the code your final DAG should look something like:

```python
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def print_world():
    print('world')


default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2017, 6, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='airflow_tutorial_v01',
    default_args=default_args,
    schedule_interval='0 * * * *'
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

print_hello >> sleep >> print_world
```


### Test the DAG

First check that DAG file contains valid Python code by executing the file with Python:

```bash
python airflow_tutorial.py
```

You can manually test a single task for a given `execution_date` with `airflow test`:

```bash
airflow test airflow_tutorial_v01 print_world 2018-10-11
```

This runs the task locally as if it was for 2018-10-11, ignoring other tasks and without communicating to the database.


### Activate the DAG

Copy your DAG to dags folder if not already. Once the scheduler is up and running, refresh the DAGs page in the web UI. You should see `airflow_tutorial_v01` in the list of DAGs with an on/off switch next to it. Turn on the DAG in the web UI and sit back while Airflow starts backfilling the dag runs!


## Exercises

You now know the basics of setting up Airflow, creating a DAG and turning it on; time to go deeper!

* Change the schedule interval to every 2 minutes.
* Add a task that prints current date using `BashOperator` or `PythonOperator`.
