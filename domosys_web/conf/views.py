#-*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.core.context_processors import csrf
from django.forms import ModelForm
import sys, json
from conf.models import Actuator, Sensor, Caption

class Config(TemplateView):
	template_name = 'conf/config.html'
	def get(self, request, *args, **kwargs):
#		if request.is_ajax():
		return render_to_response( 'conf/config.html', 
			{ 
				'actuator_list': Actuator.objects.all(), 
				'sensor_list': Sensor.objects.all(), 
			})

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)
	
class ActuatorEntryForm(ModelForm):
	class Meta:
		model = Actuator
class SensorEntryForm(ModelForm):
	class Meta:
		model = Sensor

def get_caption_form_by_type( caption_type, caption_id = 0, post=None ):
	Caption = None
	instance = None
	if caption_type == "actuator":
		Caption = Actuator
		EntryForm = ActuatorEntryForm
	elif caption_type == "sensor":
		Caption = Sensor
		EntryForm = SensorEntryForm
	if caption_id >0 :
		instance = Caption.objects.get( pk=caption_id )
	if post:
		return EntryForm( post, instance=instance )
	return EntryForm( instance=instance )

class EntryFormView(TemplateView):
	template_name = 'conf/entryform.html'
	def get(self, request, *args, **kwargs):
		sys.stderr.write("GETTING\n")
		context = {}
		context.update(csrf(request))
		if request.is_ajax():
			form = get_caption_form_by_type( kwargs['caption_type'], int(kwargs['caption_id']) )

		context.update({'form': form})
		return render_to_response( 'conf/entryform.html', context)
	
	def post(self, request, *args, **kwargs):
		sys.stderr.write("POSTING\n")
		context = {}
		context.update(csrf(request))
		if request.is_ajax():
			form = get_caption_form_by_type( kwargs['caption_type'], int(kwargs['caption_id']), request.POST )
			sys.stderr.write("form with request.POST\n")

		if form.is_valid() and not form.data.has_key('action'):
			sys.stderr.write("form save\n")
			form.save()
		else:
			if form.data['action'] == "delete":
				form.instance.delete()
			sys.stderr.write("form delete\n")
		context.update({'form': form})
		return Config.as_view()(request)

