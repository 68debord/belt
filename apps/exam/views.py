from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from datetime import datetime

from django.utils.dateformat import DateFormat 
from django.utils.formats import get_format



# Create your views here.
from models import *

def index(request):

	return render(request, 'exam/index.html')

def tasks(request):
	now = datetime.now()
	nowf = DateFormat(now)
	nowb = nowf.format(get_format('DATE_FORMAT'))
	request.session['now'] = nowb
	nowc = nowf.format(get_format('Y-m-d'))	
	today = Task.objects.filter(date = nowc)
	nottoday = Task.objects.all().exclude(date = nowc)

	return render(request, 'exam/tasks.html', 	{"today": today, "nottoday": nottoday})

def process(request):
	if request.method == "POST":
		errors = User.objects.task_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/tasks/')	
		else:		
			creator = User.objects.get(id=request.session['id'])
			Task.objects.create(creator=creator, name=request.POST['name'], status='pending', date=request.POST['date'], time=request.POST['time'])
			trial = Task.objects.last()
			compare = Task.objects.all()
			for task in compare:
				if task.date == trial.date and task.time == trial.time:
					errors["task"] = "you already have a task at this time"
					trial.delete()

		return redirect ('/exam/tasks/')
	else: 
		return redirect('/exam/tasks/')

def toggle(request):
	if request.method == "POST":

		if request.session['edit'] == True:
			request.session['edit'] = False

		else: 
			request.session['edit'] == False
			request.session['edit'] = True

		request.session['editid'] = request.POST['id']
		print request.session['edit']
		print request.session['editid']
		a = Task.objects.get(id=request.POST['id'])
		request.session['editname'] = a.name

		return redirect ('/exam/tasks/')
	else: 
		return redirect('/exam/tasks/')

def edit(request):
	if request.method == "POST":
		errors = User.objects.task_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/tasks')	
		else:			
			task = Task.objects.get(id=request.session['editid'])
			task.name = request.POST['name']
			task.status = request.POST['status']
			task.date = request.POST['date']
			task.time = request.POST['time']
			task.save()
			request.session['edit'] = False
		return redirect ('/exam/tasks/')
	else: 
		return redirect('/exam/tasks/')

def delete(request):
	if request.method == "POST":
		task = Task.objects.get(id=request.POST['id'])
		task.delete()
		return redirect('/exam/tasks')
	else:
		return redirect('/exam/tasks')	










def register(request):

	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/')	
		else:

			hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			new_user=User.objects.create(name=request.POST['name'], email=request.POST['email'], password = hashed, date_of_birth=request.POST['date_of_birth'])
			request.session['id'] = new_user.id
			request.session['name'] = new_user.name

			return redirect('/exam/tasks/')
	else:
		return redirect('/exam/')

def login(request):
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/')	
		else:
			user = User.objects.filter(email=request.POST['email'])
			request.session['id'] = user[0].id
			request.session['name'] = user[0].name
			return redirect('/exam/tasks/')
	else:
		return redirect('/exam/')

def logout(request):
	request.session['id'] = None
	request.session['name'] = None

	return redirect('/exam/')
