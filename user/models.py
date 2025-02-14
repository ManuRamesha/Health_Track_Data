# these are django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import date


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?(91?|0?)[6789]\d{9}$', 
        message="Phone number must be entered in the format: '+91xxxxxxxxxx'. Up to 13 digits allowed."
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[phone_regex], unique = True)
    parent_name = models.CharField(max_length=100, null=True, blank=True)
    parent_phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[phone_regex], unique= True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_regex = RegexValidator(
        regex=r'^[1-9][0-9]{5}$',
        message="Zip code must be entered in the format: 'xxxxxx'. Up to 6 digits allowed."
    )
    zip_code = models.CharField(max_length=6, null=True, blank=True, validators=[zip_regex])
    country = models.CharField(max_length=100, null=True, blank=True,default='India',editable=False)

    role = models.ForeignKey('tables.Role', on_delete=models.DO_NOTHING, null=True, blank=True,default="R02", related_name= "role")
    gender = models.ForeignKey('tables.Gender', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="gender")
 
    is_active = models.BooleanField(default=True)

    age = models.IntegerField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

        if self.role and self.role.role_id == "R01":
            self.is_staff = True
            self.is_superuser = True

        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username