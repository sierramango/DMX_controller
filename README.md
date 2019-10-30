# DMX_controller

Python enabled DMX controller that can be run from the Raspberry Pi and controlled wirelessly over WiFi.
<br><br>
This is a python program to send DMX signal from a serial port over RS232 to RS485 chip straight into any DMX enabled fixtures.
<br><br>
It can be controlled through any browser as long as you are connected to the raspberry pi and you know it's IP address or a hostname.
<br><br>
There are 512 sliders to control the values and there is a way to control in groups (every 3rd channel, every 4th channel, all channels...)
<br><br>
Your raspberry Pi has to be set up to run two files app.js (a node js server file) and script.py (python loop) file at startup
<br><br>
Prerequisite &
Step by step tutorial:
<br>
<br>In your linux OS, set up boot to console
<br>Change default password
<br>Set a hostname that you can connect to later instead of the IP address
<br>
<br>Through apt-get (install) or yum or any other package manager install the following packages:
<br>
<br>Install samba
<br>Install python-cherrypy3
<br>Install python-bottle
<br>Install python-serial
<br>Install nodejs
<br>Install npm
<br>Install hostapd
<br>Install isc-dhcp-server
<br>Install dnsmasq
<br>run command npm install connect
<br>run command npm install serve-static
<br>run command sudo chmod 777 /dev/ttyUSB0 this is in case you are using USB to DMX device instead of a serial chip
<br>
<br>Set Wifi to AP (from client to access point mode so it creates it's own Wifi)
<br>
<br>On every boot, run sudo nodejs /home/username/cc/app.js
<br>On every boot, run python /home/username/cc/script.py
<br>
<br>![alt text](https://github.com/sierramango/DMX_controller/raw/master/User%20Interface.png)
<br>
<br>![alt text](https://github.com/sierramango/DMX_controller/raw/master/IMG_1761.jpg)
<br>
<br>![alt text](https://github.com/sierramango/DMX_controller/raw/master/IMG_1763.jpg)
<br>
<br>![alt text](https://github.com/sierramango/DMX_controller/raw/master/IMG_1764.jpg)
