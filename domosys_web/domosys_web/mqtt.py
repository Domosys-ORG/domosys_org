#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Damien Ulrich <dams@domosys.org>'
__version__ = '0.1'
__license__ = 'GNU General Public License version 3 or later'
#__website__ = 'http://www.domosys.org/websvn'

import sys
#sys.path.append( "/usr/local/python" )

import threading
from mosquitto import Mosquitto
from time import sleep as delay

class MQTT(Mosquitto):
	def __init__(self, config):
		self.config = config
		Mosquitto.__init__( self, config['client'] )

		self.__init_mqtt_callbacks()
		self.connect(config['server'])
		self.__init_channels(config['channels'])
		self.live = threading.Thread( target = self.live_threaded )
		self.live.start()
	
	def __init_channels(self, channels):
		for channel in channels:
			if channel != "":
				self.subscribe(channel)

	def __init_mqtt_callbacks(self):
		self.on_connect = self.connected
		self.on_disconnect = self.disconnected
		self.on_publish = self.published
#		self.on_message = self.messaged
		self.on_subscribe = self.subscribed
		self.on_unsubscribe = self.unsubscribed
	

	def live_threaded(self):
		self._keep_alive = True
		while self._keep_alive:
			self.loop()
#			delay(1)
		self.disconnect()
		
	def connected(self, mosq, obj, rc):
		if rc == 0:
			self.toprint("Connected successfully.")
		else:
			self.toprint("Connection failed")

	def disconnected(self, mosq, obj, rc):
		self.toprint("Disconnected successfully.")

	def published(self, mosq, obj, mid):
		self.toprint("Message "+str(mid)+" published.")

#	def messaged(self, mosq, obj, msg):
#		print "Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload
#		print "'%s'"%msg.topic
#		if msg.topic == "ardusb/2":
#			print msg.topic, msg.payload
#		elif msg.topic == "ardusb/3":
#			print msg.topic, msg.payload

	def subscribed(self, mosq, obj, mid, qos_list):
		self.toprint("Subscribe with mid "+str(mid)+" received.")

	def unsubscribed(self, mosq, obj, mid):
		self.toprint("Unsubscribe with mid "+str(mid)+" received.")

	def toprint(self, text):
		print "%s: MQTT: %s" % (self.config['client'], text)
		sys.stdout.flush()

	
