# Importing Modules

import os
import time
import csv
from keypad import read_keypad
import display
import evdev
import sys

from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint

# Subject

subject = ""

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

# Select Subject
def subject_select(): 
	global subject
	display.draw([
	"SELECT SUBJECT",
	"1 - BSCH101 CHEM",
	"2 - BSM201 MATH",
	"3 - ESCS201 COMP",
	"4 - HMHU201 ENG"
	])
	sleep(0.2)

	while True:
		if read_keypad() == "1":
			subject = "BSCH101"
			break
		if read_keypad() == "2":
			subject = "BSM201"
			break
		if read_keypad() == "3":
			subject = "ESCS201"
			break
		if read_keypad() == "4":
			subject = "HMHU201"
			break
	display.draw(["SELECTED", subject])
	print("SELECTED " + subject)
	sleep(1)

#Shows The number of fingerprints
def show_data(): 
	print('COUNT: ' + str(f.getTemplateCount()) + '\n')
	print("SUBJECT: " + subject)
	display.draw([
	"COUNT: " + str(f.getTemplateCount()),
	"SUBJECT: " + subject
	])
	sleep(2)
	
#Clears the database 
def clear_database(): 
	f.clearDatabase()
	display.draw(["DATA CLEARED"])
	file1 = open('studentdata.csv','w')
	file1.close()
	print('All Data Cleared\n')
	sleep(3)
		
#Takes attendance
def attendance(): 
	if subject == "": subject_select()
	time_tuple = time.localtime()
	samay = time.strftime('%H:%M', time_tuple)
	print('TIME: ',samay)
	
	try:
		print('PLACE FINGER...\n')
		time.sleep(1)
	
		while (f.readImage() == False):
			display.draw([
			"PLACE FINGER",
			"SUBJECT: " + subject,
			"TIME:" + samay,
			"DATE: " + date
			])
			pass
		
		f.convertImage()  
		result = f.searchTemplate()
		
		if result[0] == -1:
			print('NO MATCH TRY AGAIN...' + '\n')
			display.draw([
			"NO MATCH",
			"TRY AGAIN..."
			])
			sleep(3)
			return None
		
		else:
			if not os.path.exists(f'data/{date}_{subject}.csv'):
				with open(f'data/{date}_{subject}.csv', 'w') as file2:
					csvout = csv.writer(file2)
					csvout.writerow(['Roll','Name','Subject','Time In','Time Out'])
	
			print('FOUND TEMPLATE' + str(result[0]+1) + '\n')
		
			with open('studentdata.csv','r') as file1:
				with open(f'data/{date}_{subject}.csv', 'r') as file2:
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
					
			display.draw([
			"REGISTERING...",
			"NAME: " + name,
			"ROLL: " + roll,
			"DEPT: " + dept,
			"YEAR: " + year
			])		
			sleep(3)  
			
		with open(f'data/{date}_{subject}.csv', 'r') as file:
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
        
		with open(f'data/{date}_{subject}.csv', 'w') as file:
			writer = csv.writer(file)
			writer.writerows(rows)
									
	except Exception as e:
		print('Operation Failed- Exception message: '+str(e) + '\n')       

#Main Menu
def main_menu() :
	while True:
		display.draw([
		"1 - ATTENDANCE",
		"2 - SELECT SUBJECT",
		"3 - SHOW DATA",
		"4 - SHUT DOWN"
		])
			
		if read_keypad() == "1": 
			attendance()
		if read_keypad() == "2": 
			subject_select()
		if read_keypad() == "3": 
			show_data()
		if read_keypad() == "4":
			return 1

# Main Funtion
if __name__ == '__main__':
	if main_menu() == 1:
		os.system("sudo shutdown now")
		sys.exit()

