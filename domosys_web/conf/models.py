from __future__ import absolute_import, unicode_literals
from django.db import models

class Room(models.Model):
	room = models.CharField("Room", max_length="16")
	
	def __unicode__(self):
		return unicode(self.room)

class Caption(models.Model):
	''' 
		caption_id = room-name
		mqtt_status = status/room/name
	'''
	name = models.CharField('Nom', max_length="16")
	_room = models.ForeignKey('Room')

	@property
	def room(self):
		return self._room.room
		
	@property
	def caption(self):
		return '-'.join([self.room, self.name])

	def __unicode__(self):
		return unicode(self.caption)

	@property
	def mqtt_status(self):
		return 'status/%s' % '/'.join([self.room, self.name])
	
	class Meta:
		abstract = True

ACTUATORS_TYPES = ( ('0', None), ('1', "pwm"), ('2', "onoff"), ('3', "offonhigh") )
class Actuator(Caption):
	''' 
		cellier-vmc
		salon-white
		salon-cool
		sejour-sculpture
		plantes-light
		plantes-ventilation
	'''
	actuator_type = models.CharField("Type", max_length=16, choices=ACTUATORS_TYPES, default='0')
	
	def __unicode__(self):
		return unicode(self.caption)

	@property
	def mqtt_channel(self):
		return '/'.join([self.room, self.name])

SENSORS_TYPES = ( ('0', None), ('1', "temperature") )
class Sensor(Caption):
	''' 
		cellier-temperature
		sejour-temperature
	'''
	sensor_type = models.CharField("Type", max_length=16, choices=SENSORS_TYPES, default='0')

#class Alias(models.Model):
#	name = models.CharField('Nom', max_length=32)
#	

#RULES = ( ('0', '=='), ('1', '!='), ('2', '<'), ('3', '>'), ('4', '<='), ('5', '>='))
#class Scenars(models.Model):
#	name = models.CharField('Nom', max_length=32)
#	caption = models.ForeignKey('Caption')
#	rule = models.CharField("Rule", max_length=2, choices=RULES, default='0')
#	value = models.Charfield
	
	
	
	
	
