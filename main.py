import json
from time import sleep
from pyKamstrup.main import Kamstrup
from paho.mqtt.client import Client

vars = {

	0x0001: "Energy in",
	0x0002: "Energy out",

	0x000d: "Energy in hi-res",
	0x000e: "Energy out hi-res",

	0x041e: "Voltage p1",
	0x041f: "Voltage p2",
	0x0420: "Voltage p3",

	0x0434: "Current p1",
	0x0435: "Current p2",
	0x0436: "Current p3",

	0x03ff: "Power In",
	0x0438: "Power p1 In",
	0x0439: "Power p2 In",
	0x043a: "Power p3 In",

	0x0400: "Power Out",
	0x0540: "Power p1 Out",
	0x0541: "Power p2 Out",
	0x0542: "Power p3 Out",
}

values = {}
units = {}

pwrMeter = Kamstrup(serial_port="/dev/ttyUSB0")
mqttClient = Client("power_meter")
broker_address = "<IP ADDRESS>"

while True:
	print("Fetching data from meter..")
	for i in vars:
		val, unit = pwrMeter.readvar(i)
		values[vars[i]] = val
		units[vars[i]] = unit

	mqttClient.connect(broker_address)
	print("MQTT client connected.")
	print("Publishing data:...")
	mqttClient.publish("homeassistant/sensor/main-power-meter/data", json.dumps(values))
	print("Data published:" + json.dumps(values))
	mqttClient.disconnect()
	print("Client disconnected.")
	sleep(15)
