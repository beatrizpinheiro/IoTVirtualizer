from datetime import datetime, timedelta
import logging
from time import sleep
from sender import Sender
from cataloguer import Cataloguer
from register import Register
from datetime import datetime
from dataProcessor import DataProcessor
from database import (
    VirtualRes,
    Capabilities,
    ResourceCapability,
    RealSensors,
    SensorData,
)
import json
import pika
import csv
import time


class Manager(object):
    def __init__(self):
        print("[MANAGER] MANAGER INICIADO")
        self.sender = Sender()
        self.register = Register()
        self.cataloguer = Cataloguer()
        self.dataProcessor = DataProcessor()

    def manageSendData(self, data):
        print("[MANAGER] Envio de dados Iniciado")
        return self.sender.sendData(data)

    def manageRegistResource(self, data, channel, connection):
        try:
            response = self.register.regData(data)
            response = json.loads(response)

            # if(response["realSensors"] != None):
            #    self.register.regIoTGateway(data) #cadastra no iot gateway

            if response != -1:
                resource = self.cataloguer.saveResource(
                    data, response, channel, connection
                )
                return resource
        except Exception as e:
            print(e)
            return -1

    def manageRegistCapability(self, data, channel, connection):
        capability = {
            "name": data["name"],
            "description": data["description"],
            "capability_type": "sensor",
        }
        response = self.register.regCap(capability)
        if response != -1:
            capability = self.cataloguer.saveCapability(data, channel, connection)
            return capability
        return -1

    def manageDataProcess(self, data, channel, connection):
        try:
            response = self.cataloguer.saveData(data, channel, connection)
            return response
        except:
            return "[MANAGER] Erro no processo de recebimento de dados"

    def callback(self, ch, method, properties, body):
        logging.info(" [x] Received %r" % body.decode())
        time.sleep(body.count(b"."))
        logging.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        uuid = ((str)(body.decode()).split(";")[0]).split(":")[0]
        neighborhood = ((str)(body.decode()).split(";")[0]).split(":")[1]
        average = (str)(body.decode()).split(";")[1]

        data = {
            "data": {
                "environment_monitoring": [
                    {
                        "neighborhood": neighborhood,
                        "temperature": str(average),
                        "timestamp": str(datetime.now())
                    }
                ]
            }
        }
        self.sender.sendData(data, uuid)

    def processActivator(self, sleeptime):
        logging.info("[MANAGER] ProcessActivator Iniciado")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        channel = connection.channel()
        channel.queue_declare(queue="task_queue_output", durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue="task_queue_output", on_message_callback=self.callback
        )

        logging.info(" [*] Waiting for messages. To exit press CTRL+C")

        channel.start_consuming()
