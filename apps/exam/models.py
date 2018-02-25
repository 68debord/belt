from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime
from django.utils.dateformat import DateFormat 
from django.utils.formats import get_format
now = datetime.now()
nowf = DateFormat(now)
nowc = nowf.format(get_format('Y-m-d')) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+( [a-zA-Z]+)*$')
# Create your models here.
class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "name should be more than 2 characters"
        if len(postData['alias']) < 3:
            errors["alias"] = "alias should be more than 2 characters"
        if not NAME_REGEX.match(postData['name']):
        	errors["name"] = "name should be only letters"
        if not NAME_REGEX.match(postData['alias']):
            errors["alias"] = "alias should be only letters" 
        if not EMAIL_REGEX.match(postData['email']):
        	errors["email"] = "must enter valid email"  
        test = User.objects.filter(email=postData['email'])   
        if len(test) != 0:
        	errors["email"] = "email already in use"        	    	
        if len(postData['password']) < 8:
            errors["password"] = "password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "passwords must match"
        if postData['date_of_birth'] > nowc:
            errors["date_of_birth"] = "you can't be born in the future"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user) != 0:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                return errors
            else: 
                errors["password"] = "your password did not match"

        else:    
            errors["email"] = "your email was not found"

            return errors

    def quote_validator(self, postData):
    	errors = {}
    	if len(postData['quoted_by']) < 4:
    		errors["quoted_by"] = "quoted by must be more than 3 characters"
    	if len(postData['quote']) < 11:
    		errors["quote"] = "quote must be more than 10 characters"
    	return errors





class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	date_of_birth = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	objects = BlogManager()

class Quote(models.Model):
    quote = models.CharField(max_length=255)
    quoted_by = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="uploaded_quotes")
    fav_users = models.ManyToManyField(User, related_name = "fave_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
