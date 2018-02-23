from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

# Create your views here.
from models import *

def index(request):

	return render(request, 'exam/index.html')

def register(request):

	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/')	
		else:

			hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			new_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password = hashed)
			request.session['id'] = new_user.id
			request.session['first_name'] = new_user.first_name

			return redirect('/exam/success/')
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
			request.session['first_name'] = user[0].first_name
			return redirect('/exam/success/')
	else:
		return redirect('/exam/')

def success(request):
	print request.session['first_name']
	return render(request, 'exam/success.html')