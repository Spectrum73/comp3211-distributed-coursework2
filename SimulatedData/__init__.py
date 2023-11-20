import datetime
import logging
import pyodbc

import datetime
import random
from dataclasses import dataclass

import azure.functions as func


@dataclass
class Sensor:
    SensorID: int
    Temperature: int
    Wind: int
    Humidity: int
    CO2: int

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



def write_data(sensorData : Sensor, cursor : pyodbc.Cursor):
    cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?)", 
                       sensorData.SensorID, 
                       datetime.datetime.now(), 
                       sensorData.Temperature, 
                       sensorData.Wind, 
                       sensorData.Humidity, 
                       sensorData.CO2)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    
    NbrSensors: int = 20
    data: list[Sensor] = generate_data(NbrSensors)

    
    if mytimer.past_due:
        logging.info('The timer is past due!')


    returnString : str = ""
    for i in range(NbrSensors):
        returnString += (str(data[i]) + "\n")
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    #logging.info(returnString)

    connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:corin-server.database.windows.net,1433;Database=dist-sys-cwk2-db;Uid=Corin;Pwd=.Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    connection = pyodbc.connect(connectionString)
    cursor = connection.cursor()
    
    for x in range(NbrSensors):
        write_data(data[x], cursor)
    connection.commit()
