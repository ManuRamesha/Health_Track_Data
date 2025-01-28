# these are the django imports
from django.urls import path

from .views import ProfileCreateListView, ProfileRetrieveUpdateView

urlpatterns = [
    path('', ProfileCreateListView.as_view()),
    path('', ProfileRetrieveUpdateView.as_view())
]