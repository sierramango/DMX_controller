# DMX_controller

Python enabled DMX controller that can be run from the Raspberry Pi

This is a python program to send DMX signal from a serial port over RS232 to RS485 chip straight into any DMX enabled fixtures.

Your raspberry Pi has to be set up to run two files app.js (a node js server file) and script.py (python loop) file at startup

Prerequisites:
*bottle framework*,
*cherrypy server*
Step by step tutorial:

In your linux OS, set up boot to console
Change default password
Set a hostname that you can connect to later instead of the IP address

Install samba
Install python-cherrypy3
Install python-bottle
Install python-serial
Install nodejs
Install npm
Install hostapd
Install isc-dhcp-server
Install dnsmasq
run command npm install connect
run command npm install serve-static
run command sudo chmod 777 /dev/ttyUSB0 this is in case you are using USB to DMX device instead of a serial chip

Set Wifi to AP (from client to access point mode so it creates it's own Wifi)

On every boot, run sudo nodejs /home/username/cc/app.js
On every boot, run python /home/username/cc/script.py
