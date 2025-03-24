# Built-In Modules
import json
import os
# Third-Party Modules
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import mysql.connector
from faker import Faker

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
con_name = os.getenv("HOSTNAME", "Unknown")
python_version = os.getenv("PYTHON_VERSION", "Unknown")

@app.get("/")
def homepage():
    return {
        "message": f"Your API Request Is Processed By The Container ID {con_name} running Python Version {python_version}."
    }

@app.get("/getvpc")
def get_vpc_id_list(region: str):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_vpcs()
        vpc_id_list = [vpc['VpcId'] for vpc in response.get('Vpcs', [])]
        return vpc_id_list
    except Exception as e:
        return {"error": str(e)}

@app.get("/s3")
def get_s3_buckets(region: str):
    try:
        s3 = boto3.client('s3', region_name=region)
        response = s3.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]
    except Exception as e:
        return {"error": str(e)}

@app.get("/checks3")
def check_bucket(bucket_name: str, region: str):
    try:
        s3 = boto3.client('s3', region_name=region)
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
        return {"exists": bucket_name in buckets}
    except Exception as e:
        return {"error": str(e)}

@app.get("/files")
def list_files_in_bucket(bucket_name: str, region: str):
    try:
        s3 = boto3.client('s3', region_name=region)
        response = s3.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])] if 'Contents' in response else []
    except Exception as e:
        return {"error": str(e)}

@app.get("/connect_mysql")
def connect_mysql(host: str, user: str, password: str, database: str):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            connection.close()
            return {"message": "Connected to MySQL database"}
    except mysql.connector.Error as e:
        return {"error": str(e)}
    return {"error": "Failed to connect"}

@app.get("/create_table")
def create_table(host: str, user: str, password: str, database: str):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                location VARCHAR(255),
                email VARCHAR(255)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Table 'customers' created successfully"}
    except mysql.connector.Error as e:
        return {"error": str(e)}

@app.get("/insert_data")
def insert_data(host: str, user: str, password: str, database: str):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO customers (name, location, email) VALUES
            ('John', 'USA', 'john@gmail.com'),
            ('Alex', 'UK', 'alex@gmail.com'),
            ('Sue', 'Canada', 'sue@gmail.com')
        """
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Data inserted successfully"}
    except mysql.connector.Error as e:
        return {"error": str(e)}
