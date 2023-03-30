import serial.tools.list_ports
import paho.mqtt.client as mqtt
import time
import json

print("Xin chào ThingsBoard")

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "o5EhHrZqibR4IEHtL11Q"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setPump":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if jsonobj['params']:
                # print("A")
                ser.write("A".encode())
            else:
                ser.write("a".encode())
                # print("a")

            # ser.write(str(jsonobj['params']).encode())
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


#  find port com connect with mircrobit
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL CH340" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])

    print(commPort)
    return commPort

# global isMicrobitConected


# temp = 30
# humi = 50
# light_intesity = 100
# soil_moisture = 10


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[0] == "1":
            if splitData[1] == "TEMP":
                # client.publish("bbc-temp", splitData[2])
                # temp = splitData[2]
                # print(temp)
                collect_data = {'temperature': splitData[2]}
            elif splitData[1] == "HUMI":
                # client.publish("bbc-humi", splitData[2])
                # humi = splitData[2]
                collect_data = {'humidity': splitData[2]}
            elif splitData[1] == "SOIL":
                # soil_moisture = splitData[2]
                collect_data = {'light': splitData[2]}
            elif splitData[1] == "LIGHT":
                # light_intesity = splitData[2]
                collect_data = {'soilmoisture': splitData[2]}
        # elif splitData[0] == "2":
        #     if splitData[1] == "TEMP":
        #         client.publish("bbc-temp-2", splitData[2])
        #     elif splitData[1] == "HUMI":
        #         client.publish("bbc-humi-2", splitData[2])

        # collect_data = {'temperature': temp, 'humidity': humi, 'light': light_intesity, 'soilmoisture': soil_moisture}
        # temp += 1
        # humi += 1
        # light_intesity += 1
        # soil_moisture += 1
        print(collect_data)
        client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)

    except: # if given data error
        pass

mess = ""

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            print("readSerial")
            print(mess[start:end + 1])
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

isMicrobitConected = False



# def reGetPort():
#     if getPort() != "None":
#         ser = serial.Serial(port=getPort(), baudrate=115200)
#         isMicrobitConected = True
#         print(isMicrobitConected)
#
#     return True

client = mqtt.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883, 60)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

while True:
    # collect_data = {'temperature': temp, 'humidity': humi, 'light': light_intesity, 'soilmoisture': soil_moisture}
    # temp += 1
    # humi += 1
    # light_intesity += 1
    # soil_moisture += 1
    # client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    # print(isMicrobitConected)
    # print("while")

    if isMicrobitConected:
        # print("reading serial")
        readSerial()
    else:
        if getPort() != "None":
                ser = serial.Serial(port=getPort(), baudrate=115200)
                isMicrobitConected = True
                # print(isMicrobitConected)

    # print(isMicrobitConected)
    # print("sau while")
    time.sleep(1)


