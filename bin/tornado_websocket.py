#!/usr/bin/env python
#-*- coding:utf-8 -*-

#from __future__ import absolute_import
from tornado import (websocket, httpserver, ioloop, web, wsgi)

import os, sys
sys.path.append('/usr/local/share/domosys_org/domosys_web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'domosys_web.settings'
BASE_DIR = '/usr/local/share/domosys_org/domosys_web'
from django.conf import settings
settings.configure()
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#})
import django
import django.contrib.auth
import django.core.handlers.wsgi

import json

#import threading
#from mosquitto import Mosquitto
#from time import sleep as delay
from domosys_web.mqtt import MQTT
#from owfs.models import OW_Temperature

	
class WSHandler(websocket.WebSocketHandler):
	clients = set()
#	def __init__(self, application, request, **kwargs):
#		super(websocket.WebSocketHandler, self).__init__(application, request, **kwargs)
	mqtt=None
	def _init_mqtt(self):
		config = { 'server': 'localhost', 'client': 'tornado', 'channels' : ['status/#'] }
		self.mqtt=MQTT( config )
		self.mqtt.on_message = self.broadcast #self.mqtt_message
		self.mqtt.publish("status/tornado", "ready")

	def open(self):
		self.user = self.get_current_user()
		print("Client connected: %s" % self.user)
		self.write_message(u"Websocket : connection établie en tant que : %s" % self.user)
		if not self.mqtt:
			self._init_mqtt()
		self.clients.add(self)
		sys.stdout.flush()
#		self.mqtt.subscribe('status/#')

	def broadcast(self, mosq, obj, msg):
		for c in self.clients:
			print msg.topic, msg.payload
			c.write_message({ 'mqtt': {	'topic': msg.topic, 'payload': msg.payload, 'qos': msg.qos } } )
		print "Tornado received: %s: %s"%(msg.topic,msg.payload)
		sys.stdout.flush()
		

#	def mqtt_message(self, mosq, obj, msg):
#		self.write_message(json.dumps(
#			{ 'mqtt': 
#				{	
#					'topic': msg.topic,
#					'payload': msg.payload,
#					'qos': msg.qos
#				}
#			}
#		))
#		print "tornado: Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload
##		print "'%s'"%msg.topic
#		sys.stdout.flush()

	def on_message(self, message):
		print( "Received: " + message )
		try:
			json_obj = json.loads(message)
		except ValueError, e:
			self.write_message("ERROR: not json: %s" % message)
			sys.stdout.flush()
			return
		if json_obj.keys()[0] == "mqtt":
			print(type(json_obj['mqtt']['payload']))
			self.mqtt.publish(json_obj['mqtt']['topic'], str(json_obj['mqtt']['payload']))
			sys.stdout.flush()
		else:
			self.write_message("WARNING: TODO: not MQTT: %s" % message)
		sys.stdout.flush()

	def on_close(self):
		if self in self.clients:
			self.clients.remove(self)
			print("removed client")
		print("WebSocket closed")
		sys.stdout.flush()

	def get_current_user(self):
		engine = django.utils.importlib.import_module(settings.SESSION_ENGINE)
		session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
		print("session_key='%s'"%session_key)
		class Dummy(object):	pass
		django_request = Dummy()
		django_request.session = engine.SessionStore(session_key)
		user = django.contrib.auth.get_user(django_request)
		sys.stdout.flush()
		return user

	def get_django_session(self):
		''' from https://gist.github.com/bdarnell/654157 '''
		if not hasattr(self, '_session'):
			engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
			session_key = self.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)
			self._session = engine.SessionStore(session_key)
		return self._session
 
#	def get_current_user(self):
#		''' from https://gist.github.com/bdarnell/654157 '''
#		# get_user needs a django request object, but only looks at the session
#		class Dummy(object): pass
#		django_request = Dummy()
#		django_request.session = self.get_django_session()
#		user = django.contrib.auth.get_user(django_request)
#		if user.is_authenticated():
#			return user
#		else:
#			# try basic auth
#			if not self.request.headers.has_key('Authorization'):
#				return None
#			kind, data = self.request.headers['Authorization'].split(' ')
#			if kind != 'Basic':
#				return None
#			(username, _, password) = data.decode('base64').partition(':')
#			user = django.contrib.auth.authenticate(username = username, password = password)
#			if user is not None and user.is_authenticated():
#				return user
#			return None
def main():
	wsgi_app = wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
	tornado_app = web.Application([
		(r'/ws', WSHandler),
		('.*', web.FallbackHandler, dict(fallback=wsgi_app)),
	])
	http_server = httpserver.HTTPServer(tornado_app)
	http_server.listen(8080, address='green')
	print("Websocket listening at http://green:8080/ws")
	sys.stdout.flush()
	ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()

