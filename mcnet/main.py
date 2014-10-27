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

from bs4 import BeautifulSoup

from mcnet.models import *

from django.db import connection

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

def mspam(str):
	tmp = mspamlogs()
	tmp.text = str
	tmp.date = datetime.datetime.now()
	tmp.save()

def mlog(str):
	tmp = MLogs()
	tmp.text = str
	tmp.date = datetime.datetime.now()
	tmp.save()

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
	ret = HttpResponse(t.render(Context({'request':rq})))
	return ret

def register(rq):
	t = get_template("fb.html")
	login_text = login_info(rq)
	ses = rq.session.items()
	uname = rq.user.username
	ret = HttpResponse(t.render(Context({'ses':ses, 'request':rq, 'uname':uname})))
	return ret;

def cbase(rq):
	t = get_template("card_base.html")
	login_text = login_info(rq)
	
	results = []
	cname = ''
	if 'name' in rq.GET:
		cname = rq.GET['name']
		cursor = connection.cursor()
		cursor.execute("SELECT engname, engname <-> %s as dist FROM mcnet_hcard ORDER BY dist LIMIT 10;", [rq.GET['name']])
		out = cursor.fetchall()
		for o in out:
			results.append(o[0])
		#results = hcard.objects.filter(engname = rq.GET['name'])
	
	ret = HttpResponse(t.render(Context({'login_text':login_text, 'request':rq, 'results':results, 'cname':cname})))
	return ret

def getsoup(url):
	#url = "http://www.abumtgo.com/shop.cgi?command=search&log=0&cardname=" + cName.replace('/','%2F').replace(' ', '+').strip() + "&edition=0&displaystyle=list&x=0&y=0";
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page = response.read()
	soup = BeautifulSoup(page, "html5lib")
	return soup

def importEditions(rq):
	editions = []
	soup = getsoup("http://magiccards.info/sitemap.html")
	
	test = 0
	
	td = soup.find("td", attrs={'valign':"top", 'width':"33%"})
	tr = td.parent
	blocks = td.find("ul")
	
	for block in list(blocks.children):
		sets = list(block.find("ul").children)
		for set in sets:
			nm = set.find("a").string
			ed = hmtgedition.objects.filter(name = nm)
			if len(ed) > 0:
				edition = ed[0]
			else:
				edition = hmtgedition()
			edition.name = nm
			edition.short = set.find("small").string[:3]
			edition.cards_total = 0
			edition.save()
			editions.append(edition)
	
	td = list(tr.children)[1]
	blocks = td.find("ul")
	block = list(blocks)[0]
	sets = list(block.find("ul").children)
	for set in sets:
		nm = set.find("a").string
		ed = hmtgedition.objects.filter(name = nm)
		if len(ed) > 0:
			edition = ed[0]
		else:
			edition = hmtgedition()
		edition.name = nm
		edition.short = set.find("small").string[:3]
		edition.cards_total = 0
		edition.save()
		editions.append(edition)
	return HttpResponseRedirect("/cp")

def importCards(rq):
	editions = hmtgedition.objects.all()
	for edition in editions:
		mspam("Edition: '" + edition.short + "'")
		if edition.short == 'tst':
			edition.short = 'tsts'
		soup = getsoup("http://magiccards.info/" + edition.short + "/en.html")
		tr = soup.find("tr", attrs={'class':'even'})
		parent = tr.parent
		lines = list(parent.children)[1:]
		mspam("Total lines: " + str(len(lines)))
		i = 0
		for line in lines:
			i = i + 1
			if i % 2 == 1:
				continue
			words = list(line.children)
			cname = words[3].string
			#mspam("Trying to add " + str(words))
			tcard = hcard.objects.filter(engname = cname)
			if len(tcard) > 0:
				continue
			card = hcard()
			card.engname = cname
			card.save()
	cards = hcard.objects.all()
	mspam("Total cards in base: " + str(len(cards)))
	return HttpResponseRedirect("/cp")

def database_controlpanel(rq):
	t = get_template("db_cp.html")
	login_text = login_info(rq)
	usr = rq.user
	
	editions = hmtgedition.objects.all()
	cards = hcard.objects.all()
	spams = mspamlogs.objects.all().order_by('-date')[:300]
	
	ret = HttpResponse(t.render(Context({'request':rq, 'editions':editions,'cards':cards, 'spams':spams})))
	return ret

def addEdition(rq):
	nm = rq.GET['name']
	ed = hmtgedition.objects.filter(name = nm)
	if len(ed) > 0:
		edition = ed[0]
	else:
		edition = hmtgedition()
	edition.name = nm
	edition.short = rq.GET['short']
	edition.cards_total = 0
	edition.save()
	return HttpResponseRedirect("/cp")

def cardInfo(rq):
	t = get_template("card_info.html")
	cname = ""
	if not ('name' in rq.GET):
		return HttpResponse(t.render(Context({'request':rq, 'cname':cname})))
	cname = sanify(rq.GET['name'])
	
	cursor = connection.cursor()
	cursor.execute("SELECT engname, engname <-> %s as dist FROM mcnet_hcard ORDER BY dist LIMIT 1;", [cname])
	cname = cursor.fetchall()[0][0]
	
	
	ret = HttpResponse(t.render(Context({'request':rq, 'cname':cname})))
	return ret