FROM apache/airflow:2.4.3-python3.8
#FROM python:3.8

RUN pip install --user --upgrade pip
RUN pip install apache-airflow-providers-amazon==6.0.0

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY omniParser/ ./omniParser
RUN cd omniParser/
RUN pip install --no-cache-dir -e ./omniParser
#RUN  python omniParser/setup.py install && python omniParser/setup.py install

#COPY dags/omniParser/ ./dags/omniParser/
#RUN pip install -r requirements.txt and pip install --no-cache-dir -e ./dags/omniParser



# WORKDIR /omniParser
#RUN  python ./dags/omniParser/setup.py install

# FROM apache/airflow:2.3.2
# RUN pip install airflow-provider-kafka==0.1.1
