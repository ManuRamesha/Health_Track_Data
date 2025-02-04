from django.db import models
from django.utils import timezone

# Create your models here.
class DailyTrack(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='dailytrack' )
    date = models.DateField(default=timezone.now)
    break_through_bleed = models.CharField(max_length=10,choices=[('Yes','Yes'),('No','No')])
    break_through_bleed_details = models.TextField(blank=True, null=True)
    treatment_for_bleed = models.TextField(blank=True, null=True)

    inj_hemilibra = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    physiotherapy = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Daily Track - {self.date}"
