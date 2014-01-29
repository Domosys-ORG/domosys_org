#-*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def index(request):
	if request.user.is_authenticated():
		return render_to_response('index.html',
			context_instance=RequestContext(request)
		)
	else:
		return HttpResponseRedirect('login')

def login_user(request):
	sys.stderr.write("login_user\n")
	user = None
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
	except:
		pass
	if user is not None:
		if user.is_active:
				auth_login(request, user)
#			else:
#				context['error'] = 'Non active user'
#		else:
#			context['error'] = 'Wrong username or password'
	if user and user.is_authenticated():
		return redirect('base.views.index')
	else:
		return render_to_response('login.html', context_instance=RequestContext(request) )
	

