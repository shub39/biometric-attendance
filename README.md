# Biometric Attendance system with raspberry pi 4
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/raspberrypi/raspberrypi-original.svg" height="100" width="100" align="right"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="100" width="100" align="right"/>

A simple attendance system with raspberry pi 4 and fingerprint scanners. It has the following features

1. Enroll Student data and store details like name, roll, subjects, etc
2. Take attendance and store attendance data in a csv file format
3. Share the data over network with teachers <a href="https://syncthing.net/">Using Syncthing</a>


# QuickStart

1. Download copy of the code or clone it to desired path in the raspberry pi
2. Use <a href="https://linuxhandbook.com/crontab/">Crontab</a> to run *"main.py"* at startup.
3. Connect the peripherals properly (pinouts can be found easily on the web)
4. Install the below mentioned modules
5. To enroll students disable crontab, connect to the raspberry pi through <a href="https://www.realvnc.com/en/connect/download/viewer/">VNC Viewer </a> or HDMI and run *"admin.py"*. You will require a keyboard to enroll student details.


# Current Module Requirements
These two modules need to be installed via pip. I recommend installing them directly using `--break-system-packages` as setting up a virtual environment leads to problems while trying to autorun the program
1. <a href="https://pypi.org/project/pyfingerprint/">Pyfingerprint Module</a>
```bash
pip install pyfingerprint --break-system-packages
```
2. <a href="https://pypi.org/project/luma.core/">Luma Core</a>
```bash
pip install luma.core --break-system-packages
```
# How To Autorun?
As mentioned above I am using <a href="https://linuxhandbook.com/crontab/">Crontab</a> to autorun the *main.py* at startup. I am using a bash script because it just works. Make a new file in the home directory named `start.sh` and enter the following.
```bash
#!/bin/bash
cd PATH/TO/FOLDER # path to the directory where main.py is located
python3 main.py 
```
grant executable permission to the script
```bash
chmod +x start.sh
```
Open terminal and enter
```bash
crontab -e
```
select your preffered text editor and go to the last line and add
```bash
@reboot ~/start.sh
```
save and exit. Now the program should run automatically from the next boot

# Current Devices Used

<ol>
    <li><a href="https://robu.in/product/raspberry-pi-4-model-b-with-1-gb-ram/">Raspberry Pi 4 Model B</a></li>
    <li><a href="https://robu.in/product/r307-optical-fingerprint-reader-module-sensor/">R307 fingerprint scanner</a></li>
    <li><a href="https://robu.in/product/pl2303-pl2303hx-usb-ttl-module-5-pin/">ttl to USB converter</a></li>
    <li><a href="https://robu.in/product/0-96-inch-i2c-iic-oled-lcd-module-4pin-with-vcc-gnd-blue/">I2C OLED Display module</a></li>
    <li>USB C charging cable and power adapter</li>
    <li>Jumper wires</li>
</ol>

# Showcase

![image](https://github.com/shub39/fingerprint_attendance/assets/143277026/77be40a7-a433-4962-ad2a-fb686d6630e4)

![image](https://github.com/shub39/fingerprint_attendance/assets/143277026/83a091b0-aa2a-4414-b10d-03398c2db51b)




