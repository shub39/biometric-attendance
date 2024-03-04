# Biometric Attendance system with raspberry pi 4
A simple attendance system with raspberry pi 4 and fingerprint scanners. It has the following features

1. Enroll Student data and store details like name, roll, subjects, etc
2. Take attendance and store attendance data in a csv file format
3. Share the data over network with teachers <a href="https://syncthing.net/">Using Syncthing</a>


# Note

1. Use <a href="https://linuxhandbook.com/crontab/">Crontab</a> to run *"main.py"* at startup.
2. Connect the peripherals properly (pinouts can be found easily on the web)
3. Install the below mentioned modules
4. To enroll students connect to the raspberry pi through <a href="https://www.realvnc.com/en/connect/download/viewer/">VNC Viewer </a> and run *"admin.py"*


# Current Module Requirements
<a href="https://pypi.org/project/pyfingerprint/">Pyfingerprint Module</a>
<a href="https://pypi.org/project/luma.core/">Luma Core</a>

# Current Devices Used
1. Raspberry Pi 4 Model B
2. R307 fingerprint scanner
3. tty to USB converter
4. I2C OLED Display module
5. USB C charging cable and power adapter

# To Do
1. ~~fix the fingerprint scanner connection interface~~
2. ~~Make the process of enrolling students admin only~~
3. ~~integrate the 4x4 keypad~~
4. ~~integrate the oled display~~
5. ~~figure out a way to store the attendance~~
6. ~~figure out a way to share the stored attendance with teachers~~
7. ~~design the box~~
8. ~~complete it~~
9. integrate camera and face recgnition (maybe)
