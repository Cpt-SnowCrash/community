from __future__ import unicode_literals

from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User
import urllib, re


# Create your models here.

class UserProfile(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	user = models.ForeignKey(User, related_name='userprofile')
	bg = models.CharField(max_length=100, null=True, blank=True)
	about = models.CharField(max_length=200, null=True, blank=True)

		
		


class Item(models.Model):  # link between group of users in project and project permissions 
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=100, null = True, blank = True)
	url = models.CharField(max_length=100, null = True, blank = True)
	#categories = models.CharField(max_length=100, null = True, blank = True)
	posted_by = models.ForeignKey(User, related_name='items')
	post_url = models.CharField(max_length=200, null = True, blank = True)
	votes = models.IntegerField(null=True, blank=True, default=1)
	voters = models.ManyToManyField(User, related_name='upvoted_items')
	score = models.IntegerField(null=True, blank=True, default=1)

	description = models.TextField(null=True, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)


	def save(self, *args, **kw):

		k = re.sub('[^A-Za-z0-9]+', '-', self.title)


		self.post_url = k + str(self.uid)[:-20]

		super(Item, self).save(*args, **kw)

class Comment(models.Model):  # link between group of users in project and project permissions 
	uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	item = models.ForeignKey(Item, null=True, blank=True, related_name="comments")
	comment = models.ForeignKey("self", null=True, blank=True, related_name="comments")
	posted_by = models.ForeignKey(User, related_name='comments')
	votes = models.IntegerField(null=True, blank=True, default=1)
	content = models.TextField(null=True, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	
	