from machine import Pin, unique_id, reset,PWM, I2C, ADC
from umqttsimple import MQTTClient
from random import randint
import time
import ubinascii
import network
import uurequests
import _thread
import ssd1306
import json
from neopixel import NeoPixel
import motorcontrols

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

class Actions:
    
    def __init__(self, ssid, password):
     
        self.device = ubinascii.hexlify(unique_id()).decode('ascii')
        print(self.device)
        
        self.ssid = ssid
        self.password = password        
        self.connect_wifi()
        
        _thread.start_new_thread(self.regDevice, [])

        self.client = MQTTClient(self.device+"12", "broker.realbots.io")
        self.client.set_callback(self.handle_message)
        self.client.connect()
        print("connected")

        self.client.subscribe('magicRobot/'+self.device+'/ctrl')
        self.client.subscribe('magicRobot/'+self.device+'/execMode')
    
    def checkConnectivity(self):
        while True:
            net = network.WLAN(network.STA_IF)
            net.active(True)
            if net.isconnected() == False:
                print("Restarting, connection disconnected!")
                reset()
            time.sleep(3)
            
    
    def alert(self):
        buzzer = PWM(Pin(25), freq=2000)
        buzzer.duty(1)
        a = Pin(2)
        b = Pin(15)

        for i in range(4):
            a.on()
            b.off()
            buzzer.duty(20)
            time.sleep(0.5)
            buzzer.duty(1)
            b.on()
            a.off()
            time.sleep(0.5)
        buzzer.duty(1)
        a.off()
        b.off()
    
    def updateLdr(self):
        topic = 'magicRobot/'+self.device+'/adc'
        
        try:
            while True:
                
                ldr = ADC(Pin(36))
                val = ldr.read()
                
                fi = {"36" : str(val)}
                self.client.publish(topic, str(fi))
                time.sleep(2)
                
        except:
            pass
 
    def connect_wifi(self):
        net = network.WLAN(network.STA_IF)
        net.active(True)
        if (net.isconnected()):
            print("Wifi Connected")   
        else:
            try:
                net.connect(self.ssid, self.password)
            except Exception as e:
                print(e)
                raise Exception("Automatic Restart required")
                pass
            while net.isconnected() == False:
                pass

    def regDevice(self):
        try:
            data = {"id" : self.device, 'type':'iot'}
            headers = {'Content-Type': 'application/json'}
            uurequests.post(f'http://192.168.122.180:1000/regNewDevice',data=json.dumps(data), headers=headers)
            print("Reg success")
            _thread.start_new_thread(self.alert, [])
        except Exception as e:
            print('Failed to register device')
    
    def handle_message(self, topic, msg):
       
        send_cmd = msg.decode('utf-8')
        command = msg[0:2].decode('utf-8')  # ">D"
        pin_no = ord(send_cmd[2])  
     
        print(send_cmd)
        print(command)
        # Pin
        try:
            if command == ">D":
                value1 = ord(send_cmd[3])
                a = Pin(pin_no, Pin.OUT)
                a.on() if value1 == 1 else a.off()
                
            # Direct
            elif command == "DR":
                direction = msg[2:5]
                directControls.directControls(direction, 1000)
                
            # PWM
            elif command == ">A":
                value1 = ord(send_cmd[3])
                freq = ord(send_cmd[4])
                a = PWM(Pin(pin_no), freq=freq)
                a.duty(value1)
            
            # Display Text
            elif command == ">T":
                i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
                oled = ssd1306.SSD1306_I2C(128, 64, i2c)
                oled.fill(0)
                content = send_cmd.split('/.')
                print(content)
                
                # Content 0 is command which is >T and content is second
                arr = content[1].replace("'", "\"")
                arr = json.loads(arr)
                
                for i in arr:
                    oled.text(i[2], i[0], i[1])
                    
                oled.show()
            
            # NeoPixel
            elif command == 'np':
                
                pin = Pin(ord(send_cmd[3]), Pin.OUT)
                
                np = NeoPixel(pin, 10)
                start_index = send_cmd.index('[(')
                end_index = send_cmd.index(')]', start_index) + 2
                tuple_list_string = send_cmd[start_index:end_index]
                tuple_strings = tuple_list_string[2:-2].split('), (')
                final = [tuple(map(int, tpl.split(', '))) for tpl in tuple_strings]
                print(len(final))
                print(final)
                
                try:
                    for i in range(len(final)):
                        np[i] = final[i]
                        print(np[i])
                        
                    np.write()
                except Exception as e:
                    print(e)
            # Reset
            elif command == 'rs':
                # Reset Display
                i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
                oled = ssd1306.SSD1306_I2C(128, 64, i2c)
                oled.fill(0)
                oled.show()
                
                # Reset Motor
                right_motor1 = PWM(Pin(27, Pin.OUT), freq=1000)
                left_motor1 = PWM(Pin(16, Pin.OUT), freq=1000)
                left_motor1.duty(1)
                right_motor1.duty(1)
             
                # Reset LED
                Pin(2, Pin.OUT).off()
                Pin(15, Pin.OUT).off()
                Pin(16, Pin.OUT).off()
                Pin(17, Pin.OUT).off()
                Pin(18, Pin.OUT).off()
                Pin(27, Pin.OUT).off()
                
                # Reset RGB
                rgb = NeoPixel(Pin(14, Pin.OUT), 1)
                rgb.fill((0,0,0))
                rgb.write()
                reset()
        except:
            pass
                
                
    def mqtt_loop(self):
         
        while True:
            try:
                self.client.check_msg()
                time.sleep(0.025)
            except:
                pass


act = Actions("MAGICBITERS", "nevergiveup")
client = act.client

_thread.start_new_thread(act.updateLdr, [])
_thread.start_new_thread(act.checkConnectivity, [])