import datetime
import logging
import pyodbc

import datetime
import random
from dataclasses import dataclass

import azure.functions as func
from helper_functions import *



def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    
    data: list[Sensor] = generate_data(NbrSensors)

    
    if mytimer.past_due:
        logging.info('The timer is past due!')


    returnString : str = ""
    for i in range(NbrSensors):
        returnString += (str(data[i]) + "\n")
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    #logging.info(returnString)

    connection = get_db_connection()
    cursor = connection.cursor()
    
    for x in range(NbrSensors):
        write_data(data[x], cursor)
    connection.commit()
