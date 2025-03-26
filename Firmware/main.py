import network
import time
from umqtt.simple import MQTTClient
import json
from motorcontrols import directControls
from machine import PWM,Pin
#from servo import Servo

servo = PWM(Pin(33),freq=30)
rightAngle = 30
leftAngle = 90
    
servo.duty(rightAngle)


# Wi-Fi credentials
ssid = 'MAGICBITERS'
password = 'nevergiveup'

# MQTT broker details
client_id = 'magicgames1'
mqtt_server = 'broker.emqx.io'
mqtt_port = 1883
mqtt_topic = b'magicgames/1'
check_id="asdfasdfasdfasdf"
speed = 500

buzzer_pin = Pin(25, Pin.OUT)  
buzzer_pwm = PWM(buzzer_pin)


last_command_time = 0
current_command = None


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network connected:', wlan.ifconfig())

def message_callback(topic, msg):
    global last_command_time, current_command

    msg = json.loads(msg)
    if topic == mqtt_topic and msg["id"] == check_id:
        command = msg["command"]
        current_time = time.time()

        # If stop command is received, execute immediately
        if command == "stp":
            directControls("stp", 0)
            current_command = None
            return
        if command == "hit":
            servo.duty(leftAngle)
            time.sleep(0.3)
            servo.duty(rightAngle)
        # If a new command is received, cancel previous one
        if command != current_command:
            current_command = command
            last_command_time = current_time
            directControls(command, speed)

def connect_mqtt():
    client = MQTTClient(client_id, mqtt_server, mqtt_port)
    client.set_callback(message_callback)
    client.connect()
    print('Connected to MQTT broker at', mqtt_server)
    client.subscribe(mqtt_topic)
    print('Subscribed to topic', mqtt_topic)
    return client



def main():
    buzzer_pin.off()
    buzzer_pwm.duty(1)  
    connect_wifi()
    client = connect_mqtt()
    buzzer_pwm.duty(700)  
    time.sleep(0.5)  # Keep the buzzer on for 1 second
    buzzer_pwm.duty(0)  
    try:
        while True:
            client.wait_msg()
            time.sleep(0.05) 
    finally:
        client.disconnect()
        print('Disconnected from MQTT broker')

if __name__ == '__main__':
    directControls("stp",0)
    main()

