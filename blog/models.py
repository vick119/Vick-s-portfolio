# Create your models here.
from django.db import models
# from django import forms
import bcrypt
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['reg_first_name'] = "Your first name must contain at least 2 characters."
        elif not NAME_REGEX.match(postData['first_name']):
            errors['reg_first_name'] = "Your first name can only contain letters."
        if len(postData['last_name']) < 2:
            errors['reg_last_name'] = "Your last name must contain least 2 characters."
        elif not NAME_REGEX.match(postData['last_name']):
            errors['reg_last_name'] = "Your last name can only contain letters."


        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "You must enter a valid email address."

        existing = User.objects.filter(email=postData['email'])
        if len(existing) > 0:
            errors['reg_email'] = "A user with that email address already exists. Please log in or try another email address"

        if len(postData['password']) < 8:
            errors['reg_pass'] = "Your password must be a minimum of 8 characters in length."
        elif postData['password'] != postData['password_confirm']:
            errors['reg_pass'] = "Your passwords do not match."

        return errors

    def log_val(self, postData):
        errors = {}

        existing = User.objects.filter(email=postData['email'])
        if len(existing) == 0:
            errors['log'] = "Invalid username/password"
        else:
            if not bcrypt.checkpw(postData['password'].encode(), existing[0].password.encode()):
                errors['log'] = "Invalid username/password"

        return errors


class WorkoutManager(models.Manager):
    def workout_val(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = "You must include a book title."
        if len(postData['description']) < 5:
            errors['description'] = "You must write a description of at least 5 characters."
        if len(postData['instruction']) < 5:
            errors['instruction'] = "You must write an instruction of at least 5 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=45)
    UpdatedAt= models.DateField(auto_now_add=True)
    CreatedAt= models.DateField(auto_now_add=True)
    objects = UserManager()

class Workout(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    instruction = models.CharField(max_length=255)
    posted_by = models.ForeignKey(
        User, related_name="books_posted", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="workouts_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

# class GeeksForm(forms.Form): 
#     name = forms.CharField() 
#     geeks_field = forms.ImageField()