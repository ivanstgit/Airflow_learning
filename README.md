# Airflow_learning
Изучение Airflow

# env possible commands
conda create --name airflow_learning python=3.9

conda activate airflow_learning

conda deactivate airflow_learning


# dev setup (DAG & TASKS CREATING)
The commans below install airflow 2.8.1 on python 3.9 into environment
$ curl -o constraints.txt https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.9.txt

$ export AIRFLOW_HOME=$(pwd)/airflow && export AIRFLOW_CONFIG=$AIRFLOW_HOME/airflow.cfg
$ pip install "apache-airflow==2.8.1" --constraint "constraints.txt"
$ airflow standalone

Then in airflow/airflow.cfg change dags_folder = <pwd command output>/src

# dev start (separate terminals, in env!!!)
$ export AIRFLOW_HOME=$(pwd)/airflow && export AIRFLOW_CONFIG=$AIRFLOW_HOME/airflow.cfg
$ airflow webserver --port 8080
$ airflow scheduler
