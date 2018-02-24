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

        if not NAME_REGEX.match(postData['name']):
        	errors["name"] = "name should be only letters"

        if not EMAIL_REGEX.match(postData['email']):
        	errors["email"] = "must enter valid email"  
        test = User.objects.filter(email=postData['email'])   
        if len(test) != 0:
        	errors["email"] = "email already in use"        	    	
        if len(postData['password']) < 8:
            errors["password"] = "password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "passwords must match"
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

    def task_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0:
            errors["name"] = "you must give your appointment a name"
        if postData['date'] < nowc:
            errors["date"] = "you can't have an appointment in the past"

        return errors


class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	date_of_birth = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	objects = BlogManager()

class Task(models.Model):
	name = models.CharField(max_length=255)
	status = models.CharField(max_length=255)
	date = models.DateField()
	time = models.TimeField()
	creator = models.ForeignKey(User, related_name="tasks")

