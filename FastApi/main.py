#Built-In Modules
import json
import os
#Third-Party Modules
import boto3
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
import uvicorn
import mysql.connector
from faker import Faker

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
con_name = os.getenv("HOSTNAME")
python_version = os.getenv("PYTHON_VERSION")
@app.get("/")
def homepage():
    return f'Your API Request Is Processed By The Container ID {con_name} running Python Version {python_version}.'

@app.get("/getvpc")
def get_vpc_id_list(region)->list:
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_vpcs()
    vpc_id_list = []
    for vpc in response['Vpcs']:
        vpc_id_list.append(vpc['VpcId'])
    print(vpc_id_list)
    return vpc_id_list

@app.get("/s3")
def get_s3_buckets(region)->list:
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()
    bucket_list = []
    for bucket in response['Buckets']:
        bucket_list.append(bucket['Name'])
    print(bucket_list)
    return bucket_list

@app.get("/checks3")
def check_bucket(bucket_name,region):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()
    print(response)
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    if bucket_name in buckets:
        return f"{bucket_name} exists"
    else:
        return f"{bucket_name} does not exist"
    
@app.get("/files")
def list_files_in_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_objects_v2(Bucket=bucket_name)
    file_list = []
    for obj in response['Contents']:
        file_list.append(obj['Key'])
    print(file_list)
    return file_list

@app.get("/connect_mysql")
def connect_mysql(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            return "Connected to MySQL database"
        else:
            return "Failed to connect to MySQL database"
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"


@app.get("/create_table")
def create_table(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            # Create table query
            create_table_query = """
            CREATE TABLE customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                location VARCHAR(255),
                email VARCHAR(255)
            )
            """
            # Execute the create table query
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
            return "Table 'customers' created successfully"
        else:
            return "Failed to connect to MySQL database"
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"
    
@app.get("/insert_data")
def insert_data(host, user, password, database):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            # Insert data query
            insert_data_query = """
            INSERT INTO customers (name, location, email) VALUES
            ('John', 'USA', 'john@gmal.com'),
            ('Alex', 'UK', 'alex@gmail.com'),
            ('Sue', 'Canada', 'sue@gmail.com');
            """
    except mysql.connector.Error as error:
        return f"Error connecting to MySQL database: {error}"
    

