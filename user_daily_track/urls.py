# these are the django imports
from django.urls import path

from .views import DailyTrackViewCRUDView

urlpatterns = [
    path('', DailyTrackViewCRUDView.as_view(), name='daily_track_crud_view')
]