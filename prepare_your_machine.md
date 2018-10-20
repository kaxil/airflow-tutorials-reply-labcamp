# Setup your machine for the workshop

## What you should have

Your machine should have the following installed :
* Python (>2.7.10 at least for Python 2). If you are on OSX, installing homebrew and the homebrew python is highly recommended as well.

* SQLite (It should be installed on most systems)

* Upgrading pip is recommended.
    
    ```bash
    pip install --upgrade pip
    ```

**NOTE**: Apache Airflow won’t work on Windows. If you have a windows machine, please install Virtual Box/VMWare/Docker and install a Linux OS and then follow the instructions below or use Docker and install [Docker Airflow Image](https://github.com/puckel/docker-airflow).


## Setup

### Get Virtualenv

I would recommend virtualenv for testing.

```bash
pip install --upgrade virtualenv
```

### Virtualenv

```bash
rm -rf airflow_workshop
virtualenv airflow_workshop
source airflow_workshop/bin/activate
```

### Installing Airflow

The easiest way to install the latest stable version of Airflow is with ``pip``:

```bash
# You will need to export an environment variable due to a licensing issue.
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install apache-airflow
```

The current stable version is ``1.10.0``. You can install this version specifically by using

```bash
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install apache-airflow==1.10.0
```


The current list of `extras` is available at [https://airflow.incubator.apache.org/installation.html#extra-packages](https://airflow.incubator.apache.org/installation.html#extra-packages).

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

Set environment variable `AIRFLOW_HOME` to e.g. your current directory `$(pwd)`:

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


### References:
* [Installing Airflow - Official Docs](https://airflow.incubator.apache.org/installation.html)
