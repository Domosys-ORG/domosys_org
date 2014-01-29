#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'Damien Ulrich <s4mdf0o1@domosys.org>'
__license__ = 'GNU General Public License version 3 or later'

from __future__ import absolute_import

import sys, os
os.chdir("/usr/local/share/domosys_org/domosys_web")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domosys_web.settings')
from domosys_web.mqtt import MQTT

class MQTTRedis(object):
	mqtt_channel = "status/#"
	mqtt=None
	def _init_mqtt(self):
		config = { 'server': 'localhost', 'client': 'redis_store', 'channels' : ['status/#'] }
		self.mqtt=MQTT( config )
		self.mqtt.on_message = self.broadcast #self.mqtt_message
		self.mqtt.publish("status/tornado", "ready")
	
	
