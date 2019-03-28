from django.db import models
from django.core.validators import MaxValueValidator


class UserProfile(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    dob = models.DateField(blank=False)
    phone_num = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    location = models.CharField(max_length=100, blank=False)
