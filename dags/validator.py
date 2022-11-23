from airflow import DAG
from airflow.operators.python import PythonOperator
from utils import constants as const
from omniParser.omniparser.parser import OmniParser
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime


import json


# def read_hl7_from_s3(file_name, ti=None):
#     """ create connection with s3 bucket and read data from the file """
#
#     print(file_name)
#     print(type(file_name))
#     hook = S3Hook()
#     hl7_data = hook.read_key(key=file_name, bucket_name=const.SOURCE_BUCKET)
#     ti.xcom_push(key='file_name', value=file_name)
#     return hl7_data
#
#
# def parse_hl7_message(data: str):
#     """ parse hl7 segments and find missing required fields """
#     print(data)
#     print(type(data))
#     hl7 = HL7Message(data)
#     segments = json.dumps(hl7.segments_with_values, indent=4, sort_keys=False)
#     required_fields = json.dumps(
#         hl7.missing_required_fields, indent=4, sort_keys=False)
#     required_fields = json.loads(required_fields)
#     # print(segments)
#     # print(required_fields)
#     return json.dumps(len(required_fields))
#
#
# def validate_file(length_of_missing_fields: str, file_name: str):
#     """ validate then move file to another error or processed s3 bucket """
#
#     if length_of_missing_fields != "0":
#         hook = S3Hook()
#         hook.copy_object(source_bucket_key=file_name,
#                          dest_bucket_key=file_name,
#                          source_bucket_name=const.SOURCE_BUCKET,
#                          dest_bucket_name=const.ERROR_BUCKET,)
#         # hook.delete_objects(bucket=const.BUCKET_NAME,
#         #                     keys=const.FILE_NAME)
#     else:
#         hook = S3Hook()
#         hook.copy_object(source_bucket_key=file_name,
#                          dest_bucket_key=file_name,
#                          source_bucket_name=const.SOURCE_BUCKET,
#                          dest_bucket_name=const.PROCESSED_BUCKET,)


def file_validation(file_name, ti=None):
    pass


def parse_cclf_message(data: str):
    """ parse cclf meesages and converted into json using omni parser """

    schema = data.split('/')[2]
    parser = OmniParser(schema)
    source_file_path = "s3://" + const.SOURCE_BUCKET + "/" + data
    dest_file_path = "s3://" + const.PROCESSED_BUCKET + "/" + data
    parser.transform(source_file_path, dest_file_path)


def dag_success_alert(context):
    """ Call back function for dag success"""

    print(f"DAG has succeeded, run_id: {context['run_id']}")


with DAG(
    dag_id="validator",
    schedule_interval=None,
    start_date=datetime(2022, 8, 1),
    catchup=False,
) as dag:

    def run_this_func(dag_run):
        """ Fetching file names from queue_reader dag"""

        print("Chunk received: {}".format(dag_run.conf['file_name']))
        return dag_run.conf['file_name']

    fetch_list = PythonOperator(
        task_id="run_this",
        python_callable=run_this_func,
        dag=dag
    )

    file_validation = PythonOperator(
        task_id="read_hl7_from_s3",
        python_callable=file_validation,
        op_kwargs={
            'file_name': '{{ ti.xcom_pull(task_ids="run_this") }}'
        }
    )

    omni_parser = PythonOperator(
        task_id="parse_hl7_message",
        python_callable=parse_cclf_message,
        op_kwargs={
            'data': '{{ ti.xcom_pull(task_ids="read_hl7_from_s3") }}'
        }
    )

    # validate = PythonOperator(
    #     task_id="validate_message",
    #     on_success_callback=dag_success_alert,
    #     python_callable=validate_file,
    #     op_kwargs={
    #         'length_of_missing_fields': '{{ ti.xcom_pull(task_ids="parse_hl7_message") }}',
    #         'file_name': '{{ ti.xcom_pull(task_ids="read_hl7_from_s3", key="file_name") }}'
    #     }
    # )

    fetch_list >> file_validation >> omni_parser
