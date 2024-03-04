# Importing Modules

import os
import time
import csv
import RPi.GPIO as GPIO
import evdev
import sys

from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

# OLED display stuff

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

# Keyboard stuff

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialising the fingerprint sensor

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    
except Exception as e:
    f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
    
except Exception as e:
    print(str(e))
    
# Making the data folder
    
if not os.path.exists('data/'):
    os.makedirs('data/')

# Grabbing the time
 
date = time.strftime("%d-%m-%Y", time.localtime())    
    
# Funtions
	
def detect_keyboard(): #Detect keyBoard
	devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
	for device in devices:
		if "keyboard" in device.name.lower():
			return True
	return False
	
def subject_select(): # Select Subject
	with canvas(device) as draw:
		draw.text((0, 0), ":SELECT SUBJECT:", fill="white")
		draw.text((0, 20), "1 - BSCH101 Chemistry", fill="white")
		draw.text((0, 30), "2 - BSM201 Maths", fill="white")
		draw.text((0, 40), "3 - ESCS201 Computer", fill="white")
		draw.text((0, 50), "4 - HMHU201 English", fill="white")
	subjects = ["BSCH101", "BSM201", "ESCS201", "HMHU201"]
	while True:
		if read_line(L1, ["1","2","3","A"]) == "1":
			return subjects[0]
			break
		if read_line(L1, ["1","2","3","A"]) == "2":
			return subjects[1]
			break
		if read_line(L1, ["1","2","3","A"]) == "3":
			return subjects[2]
			break
		if read_line(L2, ["4","5","6","B"]) == "4":
			return subjects[3]
			break

def read_line(line, characters): # Keypad stuff
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(C1) == 1):
		print(characters[0])
		return characters[0]
	if(GPIO.input(C2) == 1):
		print(characters[1])
		return characters[1]
	if(GPIO.input(C3) == 1):
		print(characters[2])
		return characters[2]
	if(GPIO.input(C4) == 1):
		print(characters[3])
		return characters[3]
	GPIO.output(line, GPIO.LOW)
		
def attendance(): #Takes attendance
	time_tuple = time.localtime()
	samay = time.strftime('%H:%M', time_tuple)
	print('Registering finger at: ',samay)
	
	try:
		print('Place Your finger...\n')
		time.sleep(1)
	
		while (f.readImage() == False):
			with canvas(device) as draw:
				draw.text((0, 0), "PLACE YOUR FINGER", fill="white")
				draw.text((0, 10), ".................", fill="white")
				sleep(0.1)
			pass
		
		f.convertImage()  
		result = f.searchTemplate()
		
		if result[0] == -1:
			print('No Match Found Try Again...' + '\n')
			with canvas(device) as draw:
				draw.text((0, 0), "NO MATCH FOUND !", fill="white")
				draw.text((0, 10), "TRY AGAIN", fill="white")
			sleep(5)
			return None
		
		else:
			if not os.path.exists(f'data/{date}.csv'):
				with open(f'data/{date}.csv', 'w') as file2:
					csvout = csv.writer(file2)
					csvout.writerow(['Roll','Name','Subject','Time In','Time Out'])
	
			print('Found template at position #' + str(result[0]+1) + '\n')
		
			with open('studentdata.csv','r') as file1:
				with open(f'data/{date}.csv', 'r') as file2:
					csvread = csv.reader(file1)
					csvread2 = csv.reader(file2)
					csvwrite2 = csv.writer(file2)
	
					for row in csvread:
						if row[0] == str(result[0]+1):
							roll = str(row[1])
							name = str(row[2])
							dept = str(row[3])
							year = str(row[4])
							print('Roll no: ',roll)
							print('Name: ',name)
							print('Department: ',dept)
							print('Year: ',year)
							print('Time: ',samay)
							
			with canvas(device) as draw:
				draw.text((0, 0), "MATCH FOUND !", fill="white")
				draw.text((0, 10), "REGISTERING...", fill="white")
				draw.text((0, 30), name, fill="white")
			sleep(5)  
		
		subject = subject_select()
		
		with open(f'data/{date}.csv', 'r') as file:
			reader = csv.reader(file)
			rows = list(reader)
		present = 1    
		
		for i in rows:
			if i[1] == name:
				i.append(samay)
				present = 0
				break
		
		if present == 1:
			rows.append([roll,name,subject,samay])        
        
		with open(f'data/{date}.csv', 'w') as file:
			writer = csv.writer(file)
			writer.writerows(rows)
									
	except Exception as e:
		print('Operation Failed- Exception message: '+str(e) + '\n')       


# Main Funtion

if __name__ == '__main__':
	
	while True:
		with canvas(device) as draw:
			draw.text((0, 10), "1 - ATTENDANCE IN", fill="white")
			draw.text((0, 20), "2 - ATTENDANCE OUT", fill="white")
			draw.text((0, 30), "A - SHUT DOWN", fill="white")
			
		sleep(0.1)
		
					
		if read_line(L1, ["1","2","3","A"]) == "A":
			with canvas(device) as draw:
				draw.text((0, 10), "SHUTTING DOWN NOW", fill="white")
				draw.text((0, 20), "BYE BYE !!", fill="white")
			sleep(5)
			os.system("sudo shutdown now")
			break
		   
		if read_line(L1, ["1","2","3","A"]) == "1" or read_line(L1, ["1","2","3","A"]) == "2" :  
			attendance()
			sleep(3)
			   
