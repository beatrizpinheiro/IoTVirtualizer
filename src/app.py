from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response
from manager import Manager
from cataloguer import Cataloguer

import threading
import pika
import time
import csv

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resources", methods=["GET", "POST", "DELETE"])
def receiver():
    if request.method == 'GET':
        # Consulta Resources
        headers = ("id","uuid","description","capabilities","timestamp")
        resources = cataloguer.consultResource()
        return render_template("table.html", headings=headers, data=resources)
    if request.method == 'POST':
        # Cadastro novo Virtual Resource
        try:
            f = open('VIRTUALIZER_time_regist_resource.csv','a')
            writer = csv.writer(f)
            timeini = time.time()
            tempo_agora = datetime.now()

            data = request.get_json()
            response = manager.manageRegistResource(data)

            timefim = time.time()
            print("TEMPO DE EXECUÇÃO")
            print(timefim-timeini)

            row = [timefim-timeini , tempo_agora]
            writer.writerow(row)
            f.close()
            return jsonify(response.__dict__["__data__"])
        except:
            return "[Receiver] Erro no processo de cadastro de um novo Recurso Virtual\n"


@app.route("/capabilities", methods=["GET", "POST", "DELETE"])
def capabilities():
    if request.method == "GET":
        # Consulta Capabilities
        headers = ("id", "name", "description", "association")
        capabilities = cataloguer.consultCapabilities()
        return render_template("table.html", headings=headers, data=capabilities)
    if request.method == "POST":
        # Cadastro nova Capability
        try:
            data = request.get_json()
            response = manager.manageRegistCapability(data, channel, connection)
            print(response.__dict__)
            return jsonify(response.__dict__["__data__"])
        except:
            return "Erro no processo de envio\n"


@app.route("/realsensors", methods=["GET"])
def realsensors():
    if request.method == "GET":
        headers = ("id", "uuid", "description", "capabilities", "virtualresource")
        realSensors = cataloguer.consultRealSensors()
        return render_template("table.html", headings=headers, data=realSensors)


@app.route("/data", methods=["GET", "POST", "DELETE"])
def data():
    if request.method == "GET":
        # Consulta Datas
        headers = ("id", "sensor", "data", "timestamp")
        sensorsData = cataloguer.consultData()
        return render_template("table.html", headings=headers, data=sensorsData)
    if request.method == "POST":
        try:
            data = request.get_json()
            response = manager.manageDataProcess(data, channel, connection)
            return jsonify("{}", response)
        except Exception as e:
            print(e)
            return "[RECEIVER] Erro no processo de recebimento da dados do sensor"


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    manager = Manager()
    cataloguer = Cataloguer()  
    channel.queue_declare(queue="task_queue_input", durable=True)
    w1 = threading.Thread(target=manager.processActivator, args=(60,))

    w1.start()
    app.run(host="0.0.0.0", port=8000)
    connection.close()
