# these are the django imports
from django.urls import path

from .views import ProfileCRUDView

urlpatterns = [
    path('', ProfileCRUDView.as_view(), name='profile_crud_view')
]