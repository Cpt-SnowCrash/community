from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,  login 
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Item, Comment, UserProfile

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image, ImageFont, ImageDraw
import os.path
from django.conf import settings


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from datetime import datetime, timedelta, tzinfo
ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()
now = datetime.now(utc)
from math import log

import random


def login_view(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate( username = username, password = password)
		next_url = request.GET.get('next', '')
		if user is not None:
			login(request, user)
			if next_url == '':
				return redirect('/')
			else:
				return redirect(next_url)

		else:
			return render(request, 'login.html' , {'message':'Email and Password didnt match'})

	else:
		return render(request, 'login.html')


def signup_view(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username = username, password = password)
		userprofile = UserProfile.objects.create(user=user)

		foo = ['#9C27B0', '#E91E63', '#2196F3', '#009688', '#8BC34A', '#FFC107', '#455A64', '#795548', '#00BCD4', '#9C27B0', '#F44336', '#3F51B5', '#4CAF50', '#673AB7']
		userprofile.bg = random.choice(foo)
		userprofile.save()
		print(user.userprofile.all()[0].bg)

		login(request, user)
		return redirect('/')
	else:
		return render(request, 'signup.html')

def profile(request, uid):
	userprofile = UserProfile.objects.get(uid=uid)

	user = userprofile.user
	return render(request, 'profile.html', {'user':user})


def submit_comment(request, post_url):
	if request.user.is_authenticated():
		
		item = Item.objects.get(post_url=post_url)
		content = request.POST['content']
		posted_by = request.user
		comment = request.POST.get('comment')
		new_comment = Comment.objects.create(item=item, posted_by=posted_by, content=content, comment=comment)

		return redirect('/posts/'+post_url)
	else:
		return redirect('/login/?next=' +request.META.get('HTTP_REFERER'))

def home(request):
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def detail(request, post_url):
	item = Item.objects.get(post_url=post_url)
	return render(request, 'detail.html', {'item':item})


def upvote(request, post_url):
	if request.user.is_authenticated():
	    item = Item.objects.get(post_url=post_url)
	    item.votes +=1
	    item.voters.add(request.user)
	    item.save()
	    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return redirect('/login/?next=' +request.META.get('HTTP_REFERER'))



def calc(request):
	items = Item.objects.all()

	

	for i in items:
		order = log(max(abs(i.votes), 1), 10)
		a = datetime.now(utc)
		b = i.created

		t = (a-b).total_seconds()
		t = t/3600
		score = (i.votes*100000 )/t
		x = 1.1
		y = 1.2
		score = pow(i.votes, y)*100/pow(t, x)
		#score = int(round(score))
		i.score = score
		print(i.score)
		i.save()

	return HttpResponse('done')
	


def submit(request):
	if request.user.is_authenticated():
		

	    if request.method == 'POST':
	    	

		    title = request.POST['title']
		    
		    url = request.POST['url']
		    item = Item.objects.create(title=title,  url=url, posted_by=request.user)
		    return redirect('/')
		

		
	    else:
	    	
		    return render(request, 'submit.html')

	else:
		return redirect('/login/?next=' + '/submit/')




def index(request):
	q=request.GET.get('q', '')
	if q == 'newest':
		item_list = Item.objects.all().order_by('-created')
	else:
		item_list = Item.objects.all().order_by('-score')

	
	paginator = Paginator(item_list, 25) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	return render(request, 'index.html', {'items':items})


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'signup.html', {'form': form})


