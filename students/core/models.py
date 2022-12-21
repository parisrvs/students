from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_number


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
        ('N', "Non-Binary")
    ]

    CLASS_CHOICES = [
        ('01', "Class I"),
        ('02', "Class II"),
        ('03', "Class III"),
        ('04', "Class IV"),
        ('05', "Class V"),
        ('06', "Class VI"),
        ('07', "Class VII"),
        ('08', "Class VIII"),
        ('09', "Class IX"),
        ('10', "Class X"),
        ('11', "Class XI"),
        ('12', "Class XII"),
    ]

    name = models.CharField(max_length=40)
    student_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    roll_number = models.CharField(
        max_length=255,
        validators=[validate_number]
    )
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=50, validators=[validate_number])
