from django.db import models
from django.core.exceptions import ValidationError


from tables.models import Heamophilia
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='profile')
    ka_regd_no = models.CharField(max_length=20, unique=True)
    heamophilia_type = models.CharField(max_length=20, blank=True, null=True)
    percentage = models.CharField(max_length=20, null=True, blank=True,
                                  choices=[('1-10%', '1-10%'), ('10-20%', '10-20%'), ('20-30%', '20-30%'),
                                           ('30-40%', '30-40%'), ('40-50%', '40-50%'), ('50-60%', '50-60%'),
                                           ('60-70%', '60-70%'), ('70-80%', '70-80%'), ('80-90%', '80-90%'),
                                           ('90-100%', '90-100%'),('less then 1%', 'less then 1%')])
    factor = models.CharField(max_length=20, null=True, blank=True,
                              choices=[('vii', 'vii'), ('viii', 'viii'), ('ix', 'ix'),  ('xi', 'xi'),])
    inhibitor = models.CharField(max_length=20, null=True, blank=True,
                                 choices=[('yes', 'YES'), ('no', 'NO'), ])
    inhibitor_percentage = models.FloatField( null=True, blank=True,)
    target_joints = models.CharField(max_length=100,null=True, blank=True,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.inhibitor == 'yes' and self.inhibitor_percentage is None:
            raise ValidationError("Inhibitor percentage is required when inhibitor is 'yes'.")  
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


