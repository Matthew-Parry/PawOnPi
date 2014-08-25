import os
import sys
import time
import usb.core
import usb.util

packet_len=64

dev = usb.core.find(idVendor=0x1234, idProduct=0x0001)

def pack_request(*arguments):
	packet = [0x0] * packet_len
	i = 0
	for arg in arguments:
		packet[i] = arg
		i += 1
	return ''.join([chr(c) for c in packet])

if dev is None:
	raise ValueError('Device not found')

try:
	dev.detach_kernel_driver(0)
	print("detached")
except:
	True

dev.set_configuration(1)

piMode = pack_request(0x23,0x50) # #P = PiMode only send when sent to

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

#Setup Pi Mode
dev.write(1,piMode,0) #set FlowPaw into Pi Mode
test=dev.read(0x81,64)
#Setup Claws
dev.write(1,setup8x8,0) #8x8 on Claw2
test=dev.read(0x81,64)

dev.write(1,setupBuz,0)#Buzzer on Claw 4
test=dev.read(0x81,64)

dev.write(1,ledsOff,0) #Leds off
test=dev.read(0x81,64)

dev.write(1,playTune5,0) #Play Tune 5
test=dev.read(0x81,64)


for i in range(5): #draw matrix squares
  dev.write(1,f1,0)
  test=dev.read(0x81,64)
  dev.write(1,f2,0)
  test=dev.read(0x81,64)
  dev.write(1,f3,0)
  test=dev.read(0x81,64)
  dev.write(1,f4,0)
  test=dev.read(0x81,64)
  dev.write(1,zero,0)
  test=dev.read(0x81,64)
  
     
dev.write(1,paw,0) #Scroll text
test=dev.read(0x81,64)

dev.write(1,ledsOn,0) #leds on
test=dev.read(0x81,64)

dev.write(1,playTune9,0) #Play Tune 9
test=dev.read(0x81,64)

dev.write(1,ledsOff,0) #leds off
test=dev.read(0x81,64)


print("done")
