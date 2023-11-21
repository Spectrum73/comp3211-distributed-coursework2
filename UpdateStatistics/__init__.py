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

def main(changes):
    logging.info('Python HTTP trigger function processed a request.')

    connection = get_db_connection()
    cursor = connection.cursor()

    analysedSensors : list[Sensor, Sensor, Sensor] = []

    for i in range(NbrSensors):
        # instantiated as -999 as it is unfair to compare against 0 and we need to set as the first value we get
        # -999 is suitable as realistically none of these fields should EVER have these values
        minimumSensor : Sensor = Sensor(i+1, -999, -999, -999, -999)
        maximumSensor : Sensor = Sensor(i+1, -999, -999, -999, -999)
        averageSensor : Sensor = Sensor(i+1, 0, 0, 0, 0)

        cursor.execute(f"SELECT SensorID, Temperature, Wind, Humidity, CO2 FROM sensor_data WHERE SensorID={i+1}")
        for sensorDataInstance in cursor.fetchall():
            # Temperature Analysis
            if (minimumSensor.Temperature > sensorDataInstance.Temperature or minimumSensor.Temperature == -999): 
                minimumSensor.Temperature = sensorDataInstance.Temperature
            if (maximumSensor.Temperature < sensorDataInstance.Temperature or maximumSensor.Temperature == -999): 
                maximumSensor.Temperature = sensorDataInstance.Temperature
            averageSensor.Temperature += sensorDataInstance.Temperature
    
            # Wind Analysis
            if (minimumSensor.Wind > sensorDataInstance.Wind or minimumSensor.Wind == -999): 
                minimumSensor.Wind = sensorDataInstance.Wind
            if (maximumSensor.Wind < sensorDataInstance.Wind or maximumSensor.Wind == -999): 
                maximumSensor.Wind = sensorDataInstance.Wind
            averageSensor.Wind += sensorDataInstance.Wind

            # Humidity Analysis
            if (minimumSensor.Humidity > sensorDataInstance.Humidity or minimumSensor.Humidity == -999): 
                minimumSensor.Humidity = sensorDataInstance.Humidity
            if (maximumSensor.Humidity < sensorDataInstance.Humidity or maximumSensor.Humidity == -999): 
                maximumSensor.Humidity = sensorDataInstance.Humidity
            averageSensor.Humidity += sensorDataInstance.Humidity

            # CO2 Analysis
            if (minimumSensor.CO2 > sensorDataInstance.CO2 or minimumSensor.CO2 == -999): 
                minimumSensor.CO2 = sensorDataInstance.CO2
            if (maximumSensor.CO2 < sensorDataInstance.CO2 or maximumSensor.CO2 == -999): 
                maximumSensor.CO2 = sensorDataInstance.CO2
            averageSensor.CO2 += sensorDataInstance.CO2
        
        averageSensor.Temperature /= NbrSensors
        averageSensor.Wind /= NbrSensors
        averageSensor.Humidity /= NbrSensors
        averageSensor.CO2 /= NbrSensors

        analysedSensors.append([minimumSensor, maximumSensor, averageSensor])

    # Wipe existing statistic data
    cursor.execute("DELETE FROM sensor_statistics")

    # Write our statistic data
    for i in range(len(analysedSensors)):
        write_statistics(analysedSensors[i], cursor)
    connection.commit()

    # Create our return string and format the data nicely
    #returnString = f""
    #for i in range(len(analysedSensors)):
    #    returnString += f"Sensor {analysedSensors[i][0].SensorID}:\n   Min:{analysedSensors[i][0]}\n   Max:{analysedSensors[i][1]}\n   Avg:{analysedSensors[i][2]}\n\n"

    #return func.HttpResponse("Hello")
