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
	if not ("logged" in rq.session):
		return '<table><tr><td><form action="/login" method="get"></td></tr><tr><td><input type="text" placeholder="Login" name="login"></input></td></tr><tr><td><input type="text" placeholder="Password" name="pass"></input></td></tr><tr><td><table><tr><td><input type="submit" value="Login"></td></form><form action="/register" method="get"><td><input type="submit" value="Register"></td></tr></table></form></table>'
	else:
		return '<table><tr><td>Logged as ' + rq.session['logged'] + '</td></tr><tr><td><form action="/logout" method="get"><input type="submit" value="Logout"></form></td></tr></table>'
	
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
	rq.session.flush()
	ret = HttpResponseRedirect("/")
	return ret

def MainPage(rq):
	t = get_template("index.html")
	login_text = login_info(rq)
	ret = HttpResponse(t.render(Context({'login_text':login_text})))
	return ret

def register(rq):
	t = get_template("index.html")
	login_text = login_info(rq)
	ret = HttpResponse(t.render(Context({'login_text':login_text})))
	return ret;