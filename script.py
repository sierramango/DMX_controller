from bottle import route, run, template, response, Bottle, hook, get, post, request, template

import time

import cherrypy

import threading

import os

#sending 0 to the entire universe at bootup
dmx_data = ''
for x in range(1, 512):
   dmx_data += '0'
   dmx_data += ','
    
dmx_data += '0'

zero = dmx_data

#color fade values from 0 to 255 - master cycle
global i
i = 0
#color fade variable that tracks where in the cycle (of 3 colors) are we
global l
l = 0

#color fade variables
global red
global green
global blue
global white

#color fade initial values at bootup
red = 0
green = 0
blue = 0
white = 0

global dmx_sending
dmx_sending = True

#master function that sends the dmx signal to the serial interface
def sendDMX():
   global dmx_sending
   while dmx_sending == True:
      global dmx_data
      global dmx_data2
      global last_value
      last_value = dmx_data
      #start of the fade loop
      #reversed_i is the decreasing value during the fade
      global i
      global l
      global red
      global green
      global blue
      global white
      global reversed_i
      reversed_i = 255 - i
      #red going down, green going up
      if l < 256:
         red = reversed_i
         green = i
         blue = 0
      #green going down, blue going up
      if l > 255 and l < 512:
         red = 0
         green = reversed_i
         blue = i
      #blue going down, red going up
      if l > 511 and l < 769:
         red = i
         green = 0
         blue = reversed_i
      #replace all r, g, b & w parts from the interface to the fade values
      if "r" in last_value: 
         dmx_data2 = dmx_data.replace('r', str(red))
         dmx_data2 = dmx_data2.replace('g', str(green))
         dmx_data2 = dmx_data2.replace('b', str(blue))
         dmx_data2 = dmx_data2.replace('w', str(white))
      else:
         dmx_data2 = dmx_data
      #turn the single string with values into list of integers
      data = (list(map(int,dmx_data2.split(','))))
      import serial
      dmxPacket = chr(0x00) + ''.join(chr(bit) for bit in data)
      initial = serial.Serial('/dev/serial0', 19200)
      #sending the first stopbit
      initial.write(chr(0x00))
      initial.close()
      dmx2 = serial.Serial('/dev/serial0', 250000, stopbits=serial.STOPBITS_TWO)
      #sending the actual dmx values
      dmx2.write(dmxPacket)
      dmx2.close()
      print data
      #add 1 to variable 1 that is looping in the master loop and it is also always the increasing value
      print i
      i = i + 1
      #once we hit 255, reset the counter
      if i == 256:
         i = 0
      print l
      l = l + 1
      #once we hit 768, the whole cycle was finished, so we reset the variable to 0
      if l == 768:
         l = 0
      #we wait 23ms before sending another DMX signal
      time.sleep(0.023)

#function that keeps checking for changes in what is coming from the web interface. If there is a change, it sends it to sendDMX function. This as well as sendDmX() are running in parrallel
def updateDMX(temp_data):
   global dmx_data
   dmx_data = temp_data
   #print "updateDMX: "
   #print dmx_data
        
@hook('after_request')
def enable_cors():
   response.headers['Access-Control-Allow-Origin'] = '*'
   response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
   response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, #X-CSRF-Token'

@route('/dmx', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/dmx', 'POST')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json' 
   postdata = request.body.read()
   #print postdata
   global dmx_data
   global zero
   if postdata[1:-1] == 'zero':
      dmx_data = zero
   else:
      dmx_data = postdata[1:-1]
   #print (dmx)

#Script for the firmware update
@route('/firmware_update', method='POST')
def do_upload():
   #define the "wrong file" message
   not_correct_file = "This is not a correct firmware file. Go <a href='http://192.168.14.1/settings'>back</a> and try again.<br />"
   upload = data = request.files.data
   name, ext = os.path.splitext(upload.filename)
   if 'cc' in name and 'zip' in ext:
      #backup home directory
      os.system('cp -R /home/username/ /home/username_backup/')
      #delete current cc directory
      os.system('rm -r /home/username/cc/')
      #saving the zip file into /home/username folder
      data.save('/home/username/',overwrite=True)
      #unzip saved zip file
      os.system('unzip -d /home/username/ -o -P z9h2rk3SUfR2 /home/username/' + upload.filename )
      print (os.path.exists("/home/username/cc/app.js"))
      #verify the new firmware and if it's not legit, remove the whole username directory and restore the old one
      if os.path.exists("/home/username/cc/script.py") and os.path.exists("/home/username/cc/app.js"):
         #delete the zip file
         os.system('rm -r /home/username/*.zip')
         #delete the backup of the username home folder
         os.system('rm -r /home/username_backup/')
         yield "You successfuly uploaded the new firmware. <br />Controller is now restarting in order to finish the update. <br />Please wait 30 seconds, then make sure you are re-connected to the correct wired or wireless network and click <a href='http://192.168.14.1'>here</a> to go back to the <a href='http://192.168.14.1'>home screen</a><br />"
         #reboot
         print ('Rebooting')
         os.system('reboot')
      else:
         #firmware does not seem to be legit, so let's delete the whole username home folder and restore the old one
         os.system('rm -r /home/username/')
         os.system('mv /home/username_backup/ /home/username/')
         yield "Error x002 <br />"
         yield not_correct_file
      #chmod username home directory to 644
      os.system('chmod 755 -R /home/username')
   else:
      yield "Error x001 <br />"
      yield not_correct_file

@route('/stop_dmx', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/stop_dmx', 'GET')
def index():
   response.content_type = 'application/json'
   global dmx_sending
   dmx_sending = False
        
@route('/stop_python', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/stop_python', 'GET')
def index():
   response.content_type = 'application/json'
   yield 'DMX program successfuly terminated'
   os.system('pkill -f script.py')

@route('/start_web_server', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/start_web_server', 'GET')
def index():
   response.content_type = 'application/json'
   yield 'Starting the Webserver'
   os.system('nodejs /home/username/cc/app.js')

@route('/stop_web_server', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/stop_web_server', 'GET')
def index():
   response.content_type = 'application/json'
   yield 'Webserver is shutting down'
   os.system('pkill -f app.js')

@route('/restart_wifi', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/restart_wifi', 'GET')
def index():
   response.content_type = 'application/json'
   yield 'Restarting WiFi'
   os.system('sudo service hostapd stop')
   time.sleep(1)
   os.system('sudo service hostapd start')

@route('/restart_device', 'OPTIONS')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'

@route('/restart_device', 'GET')
def index():
   response.content_type = 'application/json'
   yield 'Rebooting'
   os.system('reboot')

@route('/changessid', 'POST')
def index():
   ssid = request.forms.get('ssid')
   password = request.forms.get('password')
   file = open('/etc/hostapd/hostapd.conf','w') 
   file.write('interface=wlan0\n') 
   file.write('ssid=' + ssid + '\n')
   file.write('country_code=US\n')
   file.write('hw_mode=g\n')
   file.write('channel=6\n')
   file.write('macaddr_acl=0\n')
   file.write('auth_algs=1\n')
   file.write('ignore_broadcast_ssid=0\n')
   file.write('wpa=2\n')
   file.write('wpa_passphrase='+ password +'\n')
   file.write('wpa_key_mgmt=WPA-PSK\n')
   file.write('wpa_pairwise=CCMP\n')
   file.write('wpa_group_rekey=86400\n')
   file.write('ieee80211n=1\n')
   file.write('wme_enabled=1') 
   file.close()
   yield "You successfuly changed the SSID of your network. <br />Controller is now restarting in order to finish the update. <br />Please wait 30 seconds, then make sure you are re-connected to the <u>NEW</u>, CORRECT wireless network and click <a href='http://192.168.14.1'>here</a> to go back to the <a href='http://192.168.14.1'>home screen</a><br />"
   #os.system('sudo service hostapd stop')
   time.sleep(1)
   #os.system('sudo service hostapd start')
   os.system('reboot')
     
@route('/saveinterface', 'POST')
def index():
   #response.headers['Content-type'] = 'application/json'
   response.content_type = 'application/json'
   postdata = request.body.read()
   interface = postdata
   f = open('/home/username/cc/www/interface.html', 'w')
   f.write(interface)  # python will convert \n to os.linesep
   f.close()

@route('/saveinterface', 'OPTIONS')
def index():
   print("Interface Saved")
    
t1 = threading.Thread(target=updateDMX, args=(dmx_data,))
t2 = threading.Thread(target=sendDMX, args=())

t1.start()
t2.start()

#t1.join()
#t2.join()

run(host='0.0.0.0', port=5000, debug=True, server='cherrypy')

#from paste import httpserver
#httpserver.serve(host='0.0.0.0', port=5000)


