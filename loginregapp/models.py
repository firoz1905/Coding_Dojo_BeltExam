from django.db import models
import re
import bcrypt
from datetime import datetime
# Create your models here.
class UserManager(models.Manager):
    def reg_validate(self,postData):
        print("i am validating the Registration Form data now")
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX=re.compile(r'^[a-zA-Z0-9.*%!@^&]')
        ## add keys and values to errors dictionary for each invalid field
        if not postData['first_name']:
            errors['first_name']="First Name cannot be empty.It is a required field"
        if len(postData['first_name'])<2:
            errors['first_name']="First Name should be minimum atleast 2 characters"
        if not postData['last_name']:
            errors['last_name']="Last Name cannot be empty.It is a required field"
        if len(postData['last_name'])<2:
            errors['last_name']="Last Name should be minimum atleast 2 characters"
        ## strptime converts a string to date object
        ## strftime converts date to a string
        if postData['dob']:
            date_from_form=datetime.strptime(postData['dob'],"%Y-%m-%d")
            if date_from_form >= datetime.now():
                errors['dob']="Your birthday must be in the past"
            else:
                age=abs(date_from_form.year-datetime.now().year)
                print(age)
                if age < 13:
                    errors['dob']="You should be atleast 13 years old "
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="Invalid Email Address"
        verify_email=User.objects.filter(email=postData['email'])
        if verify_email:
            duplicate_email=verify_email[0]
            print(duplicate_email.email)
            errors['email']=f"{duplicate_email.email} email is already exists"
        if not postData['password'].isalnum():
            errors['password']="Password contains only characters, numbers . No special characters"
        if len(postData['password'])< 8:
            errors['password']="Password should be minimum 8 characters"
        if postData['password']!=postData['confirm_password']:
            errors['confirm_password']="Passwords should be identical"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=45)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

    def __str__(self):
        return f'ID={self.id}, first_name={self.first_name},last_name={self.last_name},email={self.email}'