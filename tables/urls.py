from django.urls import path

from .views import RoleCRUDView, GenderCRUDView

urlpatterns = [
    path('role/', RoleCRUDView.as_view()),
    path('role/<str:role_id>', RoleCRUDView.as_view()),
    path('gender/', GenderCRUDView.as_view()),
    path('gender/<str:gender_id>', GenderCRUDView.as_view()),
]