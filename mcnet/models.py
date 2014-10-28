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
	short = models.CharField(max_length=4)
	cards_total = models.IntegerField()
	def __unicode__(self):
		return self.name

class hcard(models.Model):
	engname = models.TextField()
	manacost = models.TextField()
	def __unicode__(self):
		return self.engname