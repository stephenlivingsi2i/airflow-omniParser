from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from typing import Sequence
from airflow_omniparser.omniParser.omniparser.parser import OmniParser
from airflow_multi_dagrun.operators import TriggerMultiDagRunOperator
from datetime import datetime
import json

# docker build -t stephen/custom-airflow:2.4.3-test .
template_fields: Sequence[str] = ('sqs_queue', 'max_messages', 'message_filtering_config')

#
# def list_messages(messages: str):
#     """ This is a Python function that list messages from sqs sensor """
#
#     file_list = []
#     message_list = list(eval(messages))
#     for message in message_list:
#         message_body = json.loads(message['Body'])
#         bucket_name = message_body['Records'][0]['s3']['bucket']['name']
#         file_name = message_body['Records'][0]['s3']['object']['key']
#         print(bucket_name, file_name)
#         file_list.append(file_name)
#         print(file_list)
#     return file_list
#
#


def generate_dag_run(**context):
    """ Fetching file names from list """

    file_list = context['ti'].xcom_pull(task_ids='list_messages')
    for file in file_list:
        print(file)
        yield {'file_name': file}


def fetch_file_names(messages: str):
    """ This is a Python function that fetch messages from sqs sensor """

    file_list = []
    message_list = list(eval(messages))
    for message in message_list:
        message_body = json.loads(message['Body'])
        bucket_name = message_body["detail"]["bucket"]["name"]
        file_name = message_body["detail"]["object"]["key"]
        # bucket_name = message_body['Records'][0]['s3']['bucket']['name']
        # file_name = message_body['Records'][0]['s3']['object']['key']
        print(bucket_name, file_name)
        file_list.append(file_name)
        print(file_list)
    return file_list


def task_failure_alert(context):
    """ Call back function for failure"""

    print(
        f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")


with DAG(
    dag_id="hl7_validator",
    schedule_interval='*/2 * * * *',
    start_date=datetime(2022, 8, 1),
    catchup=False,
    on_failure_callback=task_failure_alert,
) as dag:

    sqs_sensor = SqsSensor(
        task_id='sqs_test',
        poke_interval=0,
        timeout=3,
        sqs_queue='https://sqs.ap-south-1.amazonaws.com/587411779741/cclf-landing-queue',
        aws_conn_id="aws_default",
        max_messages=2,
        num_batches=2,
        soft_fail=True,
    )

    fetch_file_names = PythonOperator(
        task_id="list_messages",
        python_callable=fetch_file_names,
        op_kwargs={
            'messages': '{{ ti.xcom_pull(task_ids="sqs_test", key="messages") }}',
        }
    )

    trigger = TriggerMultiDagRunOperator(
        task_id="test_validator_dag",
        trigger_dag_id="validator",
        python_callable=generate_dag_run,
        dag=dag,
    )

    sqs_sensor >> fetch_file_names >> trigger
