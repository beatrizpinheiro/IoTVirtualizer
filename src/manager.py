from datetime import datetime, timedelta
from time import sleep
from sender import Sender
from cataloguer import Cataloguer
from register import Register
from dataProcessor import DataProcessor
from database import VirtualRes, Capabilities, ResourceCapability, RealSensors, SensorData
import json

class Manager (object):
    def __init__(self):
        print("[MANAGER] MANAGER INICIADO")
        self.sender = Sender()
        self.register = Register()
        self.cataloguer = Cataloguer()
        self.dataProcessor = DataProcessor()

    def manageSendData(self,data):
        print("[MANAGER] Envio de dados Iniciado")
        return self.sender.sendData(data)

    def manageRegistResource(self,data):
        try:     
            uuid = self.register.regData(data)
            if(uuid != -1):
                resource = self.cataloguer.saveResource(data, uuid)
                return resource
        except:
            return -1

    def manageRegistCapability(self,data):
        capability={
            "name":data["name"],
            "description":data["description"],
            "capability_type":"sensor"
        }
        response = self.register.regCap(capability)
        if(response != -1):
            capability = self.cataloguer.saveCapability(data)
            return capability
        return -1

    def manageDataProcess(self, data):
        try:
            response = self.cataloguer.saveData(data)
            return response
        except:
            return "[MANAGER] Erro no processo de recebimento de dados"

    def processActivator(self, sleepTime):
        #requisitos satisfeitos?
        processos = ResourceCapability.select()
        i=0
        while(1):
            print("[MANAGER] ProcessActivator Iniciado")
            for rescap in processos:
                cap = Capabilities.select(Capabilities.association).where(Capabilities.id==rescap.capability).get()
                cap = cap.__dict__["__data__"]
                association = cap['association'].split(":")
                # print(cap) # jsonCapabilityAssociation

                #rsensors = RealSensors.select().join(VirtualRes).where(VirtualRes == rescap.virtualresource)
                rsensors = RealSensors.select().join(VirtualRes, on=(RealSensors.virtualresource==rescap.virtualresource))
                data = SensorData.select(SensorData.data, SensorData.timestamp).where(SensorData.sensor.in_(rsensors))

                dataList = []
                qtdData = 0
                for timestamp in data.dicts():
                    diference = datetime.now() - timestamp["timestamp"]
                
                    if(diference > timedelta(minutes = 1)):
                        print("[MANAGER] Dado deletado da DB: timestamp > 1min")
                        querry = SensorData.delete().where(SensorData.timestamp == timestamp["timestamp"])
                        querry.execute()

                for value in data.dicts():
                    qtdData+=1
                    valueData = json.loads(value["data"])
                    dataList.append(valueData[association[1]])
                if(qtdData>=10):
                    print("[MANAGER] Processando Dado")
                    print(cap['association'])
                    self.dataProcessor.start(dataList, association)
            sleep(sleepTime)
            
            
