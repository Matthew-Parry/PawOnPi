# -*- coding: utf-8 -*-
# Scratch FlowPaw Arm handler by Matthew Parry 2014
#
# ScratchSender and ScratchListener classes dervived from scratch_gpio_handler 
# written by Simon Walters

from array import *
import threading
import sys
import struct
import socket
import time
import usb.core
import usb.util
import scratch

PORT = 42001
DEFAULT_HOST = '127.0.0.1'
BUFFER_SIZE = 240 
SOCKET_TIMEOUT = 1
packet_len=64

def pack_request(*arguments):
	packet = [0x0] * packet_len
	i = 0
	for arg in arguments:
		packet[i] = arg
		i += 1
	return ''.join([chr(c) for c in packet])

#hex data for leds
led1=pack_request(0x23,0x4c,0x01)
led2=pack_request(0x23,0x4c,0x02)
led3=pack_request(0x23,0x4c,0x04)
led4=pack_request(0x23,0x4c,0x08)
ledsOn=pack_request(0x23,0x4c,0x0f)
ledsOff=pack_request(0x23,0x4c,0x00)
#Setup Strings
setup8x8 = pack_request(0x23,0x58,0x02,0x03) #8x8 Led display on Claw 2
setupBuz = pack_request(0x23,0x58,0x04,0x01) #Buzzer on Claw 4
#Hex data for Buzzer tunes
playTune1 = pack_request(0x23,0x43,0x04,0x01,0x00,0x01)
playTune2 = pack_request(0x23,0x43,0x04,0x01,0x00,0x02)
playTune3 = pack_request(0x23,0x43,0x04,0x01,0x00,0x03)
playTune4 = pack_request(0x23,0x43,0x04,0x01,0x00,0x04)
playTune5 = pack_request(0x23,0x43,0x04,0x01,0x00,0x05)
playTune6 = pack_request(0x23,0x43,0x04,0x01,0x00,0x06)
playTune7 = pack_request(0x23,0x43,0x04,0x01,0x00,0x07)
playTune8 = pack_request(0x23,0x43,0x04,0x01,0x00,0x08)
playTune9 = pack_request(0x23,0x43,0x04,0x01,0x00,0x09)
#Hex data for 8x8 LED display
paw = pack_request(0x23,0x43,0x02,0x03,0x00,0x0C,0x20,0x50,0x61,0x77,0x20,0x4C,0x75,0x76,0x73,0x20,0x50,0x69,0x20) #Scroll Text
alien=pack_request(0x23,0x43,0x02,0x03,0x02,0x38,0x4c,0xce,0xfa,0xfa,0xce,0x4c,0x38) #Alien face 
f1=pack_request(0x23,0x43,0x02,0x03,0x02,0xff,0x81,0x81,0x81,0x81,0x81,0x81,0xff) 
f2=pack_request(0x23,0x43,0x02,0x03,0x02,0x00,0x7e,0x42,0x42,0x42,0x42,0x7e,0x00)
f3=pack_request(0x23,0x43,0x02,0x03,0x02,0x00,0x00,0x3c,0x24,0x24,0x3c,0x00,0x00)
f4=pack_request(0x23,0x43,0x02,0x03,0x02,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00)
zero=pack_request(0x23,0x43,0x02,0x03,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)


scrat = scratch.Scratch()


#allocate the name 'FlowPaw' to the USB device
FlowPaw=usb.core.find(idVendor=0x1234,idProduct=0x0001)

#Check to see if Paw is detected
if FlowPaw is None:
     raise ValueError("Paw not found")

try:
	FlowPaw.detach_kernel_driver(0)
	print("detached")
except:
	True

FlowPaw.set_configuration(1)
piMode = pack_request(0x23, 0x50)       #only send when sent to

#Setup Pi Mode
#FlowPaw.write(1,piMode,0) #set FlowPaw into Pi Mode
#test=FlowPaw.read(0x81,64)
#Setup Claws
#FlowPaw.write(1,setup8x8,0) #8x8 on Claw2
#test=FlowPaw.read(0x81,64)

#FlowPaw.write(1,setupBuz,0)#Buzzer on Claw 4
#test=FlowPaw.read(0x81,64)

#LED lights off
def LEDsOff():
	FlowPaw.write(1,ledsOff,0) #Leds off
	test=FlowPaw.read(0x81,64)

#LED lights off
def LEDsOn():
	FlowPaw.write(1,ledsOn,0) #Leds on
	test=FlowPaw.read(0x81,64)

FlowPaw.write(1,playTune5,0) #Play Tune 5
test=FlowPaw.read(0x81,64)

#Create a variable for duration
Duration=0.05

#Procedure to use Matrix
def LightMatrix():
    #start the movement
	FlowPaw.write(1,paw,0) #Scroll text
	test=FlowPaw.read(0x81,64)
	LEDsOn()

#Procedure to play Tune
def PlayTune():
	FlowPaw.write(1,playTune9,0) #Play Tune 9
	test=FlowPaw.read(0x81,64)

     
# to make a broadcast to scratch
#s.broadcast("from python")



class ScratchSender(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.scratch_socket = socket
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
         while not self.stopped():
            time.sleep(1.1) # be kind to cpu - not certain why :)




class ScratchListener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.scratch_socket = socket
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        global cycle_trace
        #This is main listening routine

        FlowPaw.write(1,piMode,0) #set FlowPaw into Pi Mode
        test=FlowPaw.read(0x81,64)
        #Setup Claws
        FlowPaw.write(1,setup8x8,0) #8x8 on Claw2
        test=FlowPaw.read(0x81,64)

        FlowPaw.write(1,setupBuz,0)#Buzzer on Claw 4
        test=FlowPaw.read(0x81,64)
        
        while not self.stopped():
          try:

               # to receive an update from scratch
               message = scrat.receive()
               print(message)

               # blocks until an update is received
               # message returned as  {'broadcast': [], 'sensor-update': {'scratchvar': '64'}}
               #                  or  {'broadcast': ['from scratch'], 'sensor-update': {}}
               # where scratchvar is the name of a variable in scratch
               # and 'from scratch' is the name of a scratch broadcast

               # send sensor updates to scratch
               #data = {}
               #data['pyvar'] = 123
               #for data['pycounter'] in range(60):
               #    s.sensorupdate(data)

               msgtype = message#['broadcast']    #'broadcast'
               #print msgtype

          except socket.timeout:
                     print("No data received: socket timeout")
                     continue

                   
          #Execute Paw command as per broadcast message
          if 'tune' in msgtype:
               PlayTune()
          if 'matrix' in msgtype:
               LightMatrix()

          if 'stop handler' in msgtype:
                cycle_trace = 'disconnected'
                break
                cleanup_threads((listener, sender))
                sys.exit()


def create_socket(host, port):
    while True:
        try:
            print('Trying')
            scratch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scratch_sock.connect((host, port))
            break
        except socket.error:
            print("There was an error connecting to Scratch!")
            print("I couldn't find a Mesh session at host: %s, port: %s" % (host, port)) 
            time.sleep(3)
            #sys.exit(1)

    return scratch_sock

def cleanup_threads(threads):
    for thread in threads:
        thread.stop()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = DEFAULT_HOST


cycle_trace = 'start'
while True:

    if (cycle_trace == 'disconnected'):
        print("Scratch disconnected")
        cleanup_threads((listener, sender))
        time.sleep(1)
        cycle_trace = 'start'

    if (cycle_trace == 'start'):
        # open the socket
        print('Starting to connect...')
        the_socket = create_socket(host, PORT)
        print('Connected!')
        the_socket.settimeout(SOCKET_TIMEOUT)
        listener = ScratchListener(the_socket)
        sender = ScratchSender(the_socket)
        cycle_trace = 'running'
        print("Running....")
        listener.start()
        sender.start()

    # wait for ctrl+c
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        cleanup_threads((listener,sender))
        sys.exit()
