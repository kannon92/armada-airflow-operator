import airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from armada.operators.armada import ArmadaOperator

import pendulum

with DAG(
    dag_id='my_dag',
    start_date=pendulum.datetime(2016, 1, 1, tz="UTC"),
    schedule_interval='@daily',
    catchup=False,
    default_args={'retries': 2},
) as dag:

    op = BashOperator(task_id='dummy', bash_command='echo Hello World!')
    armada = ArmadaOperator(task_id='armada', name = 'hello')
    op >> armada
