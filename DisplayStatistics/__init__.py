import datetime
import logging
import pyodbc

import datetime
import random
from dataclasses import dataclass

import azure.functions as func
from helper_functions import *

def write_statistics(sensorStatistics : list[Sensor, Sensor, Sensor], cursor : pyodbc.Cursor):
    cursor.execute("INSERT INTO sensor_statistics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        sensorStatistics[0].SensorID, 
                        sensorStatistics[2].Temperature, # AVG
                        sensorStatistics[0].Temperature, # MIN
                        sensorStatistics[1].Temperature, # MAX
                        sensorStatistics[2].Wind, # AVG
                        sensorStatistics[0].Wind, # MIN
                        sensorStatistics[1].Wind, # MAX
                        sensorStatistics[2].Humidity, # AVG
                        sensorStatistics[0].Humidity, # MIN
                        sensorStatistics[1].Humidity, # MAX
                        sensorStatistics[2].CO2, # AVG
                        sensorStatistics[0].CO2, # MIN
                        sensorStatistics[1].CO2 # MAX
                        )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection = get_db_connection()
    cursor = connection.cursor()

    returnString = f""

    for i in range(NbrSensors):
        minimumSensor : Sensor = Sensor(i+1, -999, -999, -999, -999)
        maximumSensor : Sensor = Sensor(i+1, -999, -999, -999, -999)
        averageSensor : Sensor = Sensor(i+1, 0, 0, 0, 0)

        cursor.execute(f"SELECT * FROM sensor_statistics WHERE SensorID={i+1}")
        sensorDataInstance = cursor.fetchone()
        averageSensor.Temperature = sensorDataInstance.AverageTemperature
        minimumSensor.Temperature = sensorDataInstance.MinimumTemperature
        maximumSensor.Temperature = sensorDataInstance.MaximumTemperature
        averageSensor.Wind = sensorDataInstance.AverageWind
        minimumSensor.Wind = sensorDataInstance.MinimumWind
        maximumSensor.Wind = sensorDataInstance.MaximumWind
        averageSensor.Humidity = sensorDataInstance.AverageHumidity
        minimumSensor.Humidity = sensorDataInstance.MinimumHumidity
        maximumSensor.Humidity = sensorDataInstance.MaximumHumidity
        averageSensor.CO2 = sensorDataInstance.AverageCO2
        minimumSensor.CO2 = sensorDataInstance.MinimumCO2
        maximumSensor.CO2 = sensorDataInstance.MaximumCO2

        returnString += f"Sensor {averageSensor.SensorID}:\n   Min:{minimumSensor}\n   Max:{maximumSensor}\n   Avg:{averageSensor}\n\n"
        
    return func.HttpResponse(returnString)
