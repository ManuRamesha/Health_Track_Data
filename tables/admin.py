from django.contrib import admin
from .models import Role, Gender, Heamophilia

# Register your models here.
admin.site.register(Role)
admin.site.register(Gender)
admin.site.register(Heamophilia)