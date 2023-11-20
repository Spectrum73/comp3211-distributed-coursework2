import logging

import azure.functions as func
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:corin-server.database.windows.net,1433;Database=dist-sys-cwk2-db;Uid=Corin;Pwd=.Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    connection = pyodbc.connect(connectionString)
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM sensor_data")
    connection.commit()

    #name = req.params.get('name')
    return func.HttpResponse("Table Wiped!")
