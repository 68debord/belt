from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt


from models import *

def index(request):

	return render(request, 'exam/index.html')

def home(request):
	quotes = Quote.objects.exclude(fav_users = request.session['id']).order_by('-created_at')
	favorites = Quote.objects.filter(fav_users = request.session['id'])

	return render(request, 'exam/home.html', {"quotes": quotes, "favorites": favorites})

def user(request, id):
	user = User.objects.get(id=id)
	quotes = Quote.objects.filter(uploaded_by = id)
	count = len(quotes)

	return render(request, 'exam/user.html', {"user": user, "quotes": quotes, "count": count})

def process(request):
	if request.method == "POST":
		errors = User.objects.quote_validator(request.POST)
		print errors
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/home/')
		else:			
			uploaded_by = User.objects.get(id=request.session['id'])
			Quote.objects.create(uploaded_by=uploaded_by, quote=request.POST['quote'], quoted_by=request.POST['quoted_by'])
			return redirect ('/exam/home/')
	else: 
		return redirect('/exam/home/')

def favorite(request, id):

		user = User.objects.get(id=request.session['id'])
		print user
		quote = Quote.objects.get(id=id)
		print quote
		quote.fav_users.add(user)

		return redirect ('/exam/home/')


def delete(request, id):

		quote = Quote.objects.get(id=id)
		user = User.objects.get(id=request.session['id'])
		quote.fav_users.remove(user)

		return redirect('/exam/home')




def register(request):

	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/exam/')	
		else:

			hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			new_user=User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password = hashed, date_of_birth=request.POST['date_of_birth'])
			request.session['id'] = new_user.id
			request.session['alias'] = new_user.alias

			return redirect('/exam/home/')
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
			request.session['alias'] = user[0].alias
			return redirect('/exam/home/')
	else:
		return redirect('/exam/')

def logout(request):
	request.session['id'] = None
	request.session['alias'] = None

	return redirect('/exam/')
