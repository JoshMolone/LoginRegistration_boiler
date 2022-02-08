from django.db import models
import re
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["name"] = "First name must be atleast 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be atleast 2 characters"

        if len(postData['password']) < 8:
            errors["password"] = "Password must be greater than 8 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please use a valid email address"

        check_email = User.objects.filter(email=postData['email'])
        if len(check_email) > 0:
            errors["email_use"] = "Email address is already in use"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True) 
    # VALIDATOR
    objects = UserManager()
