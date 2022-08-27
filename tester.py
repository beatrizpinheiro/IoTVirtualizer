from datetime import datetime
import requests
import json

headers = {
    "Content-type": "application/json",
}


def cadastrarRecursos():
    msg = {
        "regInfos": {
            "description": "Recurso virtual teste 2",
            "capabilities": ["averageTemperature", "averagePressure"],
            "status": "active",
            "lat": 10,
            "lon": 12,
        },
        "realSensors": [
            {
                "uuid": "709fd3e3-4112-46f4-b148-4778775998e8",
                "capabilities": ["temperature", "pressure"],
            }
        ],
    }

    response = requests.post(
        "http://10.0.2.15:8000/resources", data=json.dumps(msg), headers=headers
    )
    return response


def cadastrarCapability():
    msg = {
        "name": "averagePressure",
        "description": "Average Pressure of a region",
        "capability_type": "sensor",
        "association": "$average:pressure",
    }
    response = requests.post(
        "http://localhost:5000/capability", data=json.dumps(msg), headers=headers
    )
    return response


def sendSensorData():
    msg = {
        "uuid": "047d2160-0d56-440a-a4cc-d1f66fe7fb1e",
        "data": {
            "environment_monitoring": 
                {
                    "neighborhood": "Setor Oeste",
                    "temperature": 54,
                    "timestamp": "2017-06-14T17:52:25.428Z",
                }
            
        },
    }
    response = requests.post(
        "http://10.0.2.15:8000/data", data=json.dumps(msg), headers=headers
    )
    return response


def sendSensorData2():
    msg = {
        "uuid": "047d2160-0d56-440a-a4cc-d1f66fe7fb1e",
        "data": {
            "environment_monitoring": 
                {
                    "neighborhood": "Setor Oeste",
                    "temperature": 30,
                    "timestamp": "2017-06-14T17:52:25.428Z",
                }
            
        },
    }
    response = requests.post(
        "http://10.0.2.15:8000/data", data=json.dumps(msg), headers=headers
    )
    return response


def sendSensorData3():
    msg = {
        "uuid": "047d2160-0d56-440a-a4cc-d1f66fe7fb1e",
        "data": {
            "environment_monitoring": 
                {
                    "neighborhood": "Setor Bueno",
                    "temperature": 30,
                    "timestamp": "2017-06-14T17:52:25.428Z",
                }
            
        },
    }
    response = requests.post(
        "http://10.0.2.15:8000/data", data=json.dumps(msg), headers=headers
    )
    return response

def testesINCT():
    finaldata = {"data": {"averagePressure": [{"pressure": 1.0}]}}
    response = requests.post(
        "http://35.247.228.184:8000/adaptor/resources/"
        + "0c6573d7-eb51-4688-b2a5-2a4092799b23"
        + "/data",
        data=json.dumps(finaldata),
        headers=headers,
    )
    # response = requests.post ('http://35.247.228.184:8000/catalog/capabilities', data = json.dumps(capability),headers=headers)
    # response = requests.get('http://35.247.228.184:8000/collector/resources/data' ,headers=headers)
    return response


if __name__ == "__main__":
    response = sendSensorData()
    print(response)
    print(response.text)

    response = sendSensorData2()
    print(response)
    print(response.text)

    response = sendSensorData3()
    print(response)
    print(response.text)
