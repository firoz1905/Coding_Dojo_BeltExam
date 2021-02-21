from django.db import models
from datetime import datetime
from loginregapp.models import User
# Create your models here.
class TripManager(models.Manager):
    def trip_validate(self,postData):
        print("i am validating the trip data now")
        errors={}
        if not postData['destination']:
            errors['destination']="Destination cannot be empty !!"
        if len(postData['destination'])<3:
            errors['destination']="Enter a valid Destination.It must be atleast 4 characters"
        if len(postData['description'])<5:
            errors['description']="Description must be at atleast 5 characters"
        if not postData['from_date']:
            errors['from_date']="Travel from date cannot be empty!!"
        if postData['from_date']:
            from_date_form=datetime.strptime(postData['from_date'],"%Y-%m-%d")
            if from_date_form >= datetime.now():
                errors['from_date']="Your Travel From date cannot be in the past"
        if not postData['to_date']:
            errors['to_date']="Travel to date cannot be empty!!"
        if postData['to_date']:
            to_date_form=datetime.strptime(postData['to_date'],"%Y-%m-%d")
            if to_date_form < from_date_form:
                errors['to_date']="Your Travel to date should not be before the Travel date from "
        return errors

class Trip(models.Model):
    destination=models.CharField(max_length=45)
    description=models.CharField(max_length=255)
    from_date=models.DateTimeField()
    to_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    added_by=models.ForeignKey(User,related_name="trip_created",on_delete=models.CASCADE)
    ## added_by =User who added the trip
    users_who_join=models.ManyToManyField(User,related_name="joined_trips")
    ## users_who_join= a list of users who join a trip
    objects=TripManager()

    def __str__(self):
        return f'ID={self.id}, dest={self.destination},desc={self.description},from_date={self.from_date},to_date={self.to_date}'