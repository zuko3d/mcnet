from django.db import models

class mspamlogs(models.Model):
	text = models.TextField()
	date = models.DateTimeField()
	def __unicode__(self):
		return self.text

class MLogs(models.Model):
	text = models.TextField()
	date = models.DateTimeField()
	def __unicode__(self):
		return self.text

class hmtgedition(models.Model):
	name = models.TextField()
	short = models.TextField()
	cards_total = models.IntegerField()
	def __unicode__(self):
		return self.name

class hcard(models.Model):
	engname = models.TextField()
	snfd_name = models.TextField()
	manacost = models.TextField()
	pic = models.TextField()
	ed_info = models.TextField()# @... edition short$card no.$rarity (one letter)@
	def __unicode__(self):
		return self.engname

class mtm_card_edition(models.Model):
	engname = models.TextField()
	short = models.TextField()
	no = models.IntegerField()
	def __unicode__(self):
		return self.engname + "/" + self.short