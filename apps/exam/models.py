from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.
class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors["first_name"] = "first name should be more than 2 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "last name should be more than 2 characters"
        if not NAME_REGEX.match(postData['first_name']):
        	errors["first_name"] = "first name should be only letters"
        if not NAME_REGEX.match(postData['last_name']):
        	errors["last_name"] = "last name should be only letters" 
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




class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	objects = BlogManager()