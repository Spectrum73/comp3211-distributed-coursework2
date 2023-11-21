import logging
import io

import datetime
import azure.functions as func
import matplotlib.pyplot as plt
from PIL import Image 
from helper_functions import *
import time

# Write a defined amount of sensors with data to the database and return how long it takes
def write_n_sensors(n : int, connection : pyodbc.Connection) -> float:
    start_time = time.time()
    cursor = connection.cursor()

    sensorData = generate_data_alt(n)
    for sensor in sensorData:
        write_data_with_time(sensor, cursor, datetime.datetime.now())
    connection.commit()

    execution_time = time.time() - start_time
    remove_fake_data(connection)
    return execution_time

def remove_fake_data(connection : pyodbc.Connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sensor_data WHERE SensorID < 0")
    connection.commit()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    dataWriteBands : list[int] = [1, 5, 10, 20, 50, 100, 1000]
    connection = get_db_connection()

    x_axis = dataWriteBands
    y_axis = []

    for i in range(len(dataWriteBands)):
        time_taken = write_n_sensors(dataWriteBands[i], connection)
        y_axis.append(time_taken)


    plt.plot(x_axis, y_axis)
    plt.title('Database Performance')
    plt.xlabel('Sensors generated and written')
    plt.ylabel('Time taken')
    imgName = "performance_graph.png"
    plt.savefig(imgName)
    img = Image.open(imgName)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return func.HttpResponse(img_byte_arr, mimetype='image/png')