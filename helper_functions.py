import datetime
import logging
import pyodbc

import datetime
import random
from dataclasses import dataclass

import azure.functions as func

NbrSensors = 20
SqlConnectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:corin-server.database.windows.net,1433;Database=dist-sys-cwk2-db;Uid=Corin;Pwd=.Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

@dataclass
class Sensor:
    SensorID: int
    Temperature: int
    Wind: int
    Humidity: int
    CO2: int

# Helps need the connection string to only be defined in one place
def get_db_connection() -> pyodbc.Connection:
    connectionString = SqlConnectionString
    return pyodbc.connect(connectionString)

def generate_data(nbrSensors : int) -> list[Sensor]:
    data: list[Sensor] = []

    for i in range(nbrSensors):
        data.append(Sensor(
            i + 1,
            random.randint(8, 15),
            random.randint(15, 25),
            random.randint(40, 70),
            random.randint(500, 1500)
        ))
    return data

# Generates a set of data with negative sensor IDs
# Useful for benchmarking as the data can be removed afterwards
def generate_data_alt(nbrSensors : int) -> list[Sensor]:
    data: list[Sensor] = []

    for i in range(nbrSensors):
        data.append(Sensor(
            -i - 1,
            random.randint(8, 15),
            random.randint(15, 25),
            random.randint(40, 70),
            random.randint(500, 1500)
        ))
    return data



def write_data(sensorData : Sensor, cursor : pyodbc.Cursor):
    cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?)", 
                       sensorData.SensorID, 
                       datetime.datetime.now(), 
                       sensorData.Temperature, 
                       sensorData.Wind, 
                       sensorData.Humidity, 
                       sensorData.CO2)
    
def write_data_with_time(sensorData : Sensor, cursor : pyodbc.Cursor, time : datetime):
    cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?)", 
                       sensorData.SensorID, 
                       time, 
                       sensorData.Temperature, 
                       sensorData.Wind, 
                       sensorData.Humidity, 
                       sensorData.CO2)