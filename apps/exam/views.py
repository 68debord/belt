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

def home(request):


	return render(request, 'exam/home.html')

def process(request):
	if request.method == "POST":

		else:		

		return redirect ('/exam/tasks/')
	else: 
		return redirect('/exam/tasks/')

def edit(request):
	if request.method == "POST":

		return redirect ('/exam/tasks/')
	else: 
		return redirect('/exam/tasks/')

def delete(request):
	if request.method == "POST":
		# task = Task.objects.get(id=request.POST['id'])
		# task.delete()
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
