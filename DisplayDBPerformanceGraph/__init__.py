import logging
import io

import azure.functions as func
import matplotlib.pyplot as plt
from PIL import Image 

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    dataWriteBands : list[int] = [1, 5, 10, 20, 50, 100]

    x_axis = dataWriteBands
    y_axis = [0.1, 0.5, 1.0, 2.1, 6.0, 12.3]

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
    #return func.HttpResponse("Hello, PERSON. This HTTP triggered function executed successfully.")