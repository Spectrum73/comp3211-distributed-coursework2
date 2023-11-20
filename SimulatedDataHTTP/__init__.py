import logging

import azure.functions as func

import random
from dataclasses import dataclass

@dataclass
class Sensor:
    SensorID: int
    Temperature: int
    Wind: int
    Humidity: int
    CO2: int


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    NbrSensors: int = 20
    data: list[Sensor] = []

    for i in range(NbrSensors):
        data.append(Sensor(
            i + 1,
            random.randint(8, 15),
            random.randint(15, 25),
            random.randint(40, 70),
            random.randint(500, 1500)
        ))

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        returnString : str = ""
        for i in range(NbrSensors):
            returnString += (str(data[i]) + "\n")
        return func.HttpResponse(
             returnString,
             status_code=200
        )
