# Setup your machine for the workshop

## What you should have

Your machine should have the following installed :
* Python (>2.7.10 at least for Python 2). If you are on OSX, installing homebrew and the homebrew python is highly recommended as well.

* SQLite (It should be installed on most systems)

* Upgrading pip is recommended.
    
    ```bash
    pip install --upgrade pip
    ```

**NOTE**: Apache Airflow won’t work on Windows. If you have a windows machine, please install Virtual Box/VMWare/Docker and install a Linux OS and then follow the instructions below or directly [Docker Airflow Image](https://github.com/puckel/docker-airflow).


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


### References:
* [Installing Airflow - Official Docs](https://airflow.incubator.apache.org/installation.html)
