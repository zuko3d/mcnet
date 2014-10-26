from django.db import models
from django.contrib.auth.models import AbstractUser

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

class CustomUser(AbstractUser):
	#access flags
	af = models.TextField()
	def __unicode__(self):
		return self.text

class hmtgedition(models.Model):
	name = models.TextField()
	short = models.CharField(max_length=3)
	cards_total = models.IntegerField()
	id = models.IntegerField()

class hcard(models.Model):
	engname = models.TextField()