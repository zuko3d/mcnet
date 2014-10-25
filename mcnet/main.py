import cgi
import os
import urllib2
import re
import datetime
import django.shortcuts
import multiprocessing
import threading
import sys
import traceback
import weakref
import time 
import string
import random

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template

#from hello.models import *

def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def asc(s):
	return unicode(s).encode('ascii', 'ignore').strip()

def encrypt(str):
	ret = ""
	i = 2
	for c in str:
		ret = ret + chr((ord(c) + i) % 128)
		i = i + 1 
	return ret

def sanify(s):
	result = ""
	ascs = asc(s)
	for c in ascs:
		if c in '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-':
			result = result + c
	return result

def login_info(rq):
	if not ("_auth_user_id" in rq.session):
		return '<a href="/accounts/login">Login</a>'
	else:
		return '<table><tr><td>Logged as ' + rq.user.username + '</td></tr><tr><td><form action="/logout" method="get"><input type="submit" value="Logout"></form></td></tr></table>'
	
def login(rq):
	ret = HttpResponseRedirect("/")
	if not ('login' in rq.GET):
		return ret
	if not ('pass' in rq.GET):
		return ret
	lg = rq.GET['login']
	if lg != sanify(lg):
		return ret
	if len(lg) < 1:
		return ret
	
	rq.session['logged'] = lg
	return ret

def logout(rq):
	#rq.session.flush()
	ret = HttpResponseRedirect("/accounts/logout")
	return ret

def MainPage(rq):
	t = get_template("index.html")
	login_text = login_info(rq)
	ret = HttpResponse(t.render(Context({'login_text':login_text})))
	return ret

def register(rq):
	t = get_template("fb.html")
	login_text = login_info(rq)
	ses = rq.session.items()
	uname = rq.user.username
	ret = HttpResponse(t.render(Context({'login_text':login_text, 'ses':ses, 'request':rq, 'uname':uname})))
	return ret;

def cbase(rq):
	t = get_template("card_base.html")
	login_text = login_info(rq)
	
	ret = HttpResponse(t.render(Context({'login_text':login_text, 'request':rq})))
	return ret;