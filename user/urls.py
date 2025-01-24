from django.urls import path

from .views import RegisterUser, LoginView, AdminRegisterUser, AdminLoginView, AdminUserCRUDView


urlpatterns = [
    path('register',RegisterUser.as_view(),name='register'),
    path('login', LoginView.as_view(), name='login'),

    path('admin/register', AdminRegisterUser.as_view(), name='admin_register'),
    path('admin/login', AdminLoginView.as_view(), name='admin_login'),

    path('admin/user/', AdminUserCRUDView.as_view()),
    path('admin/user/<str:username>', AdminUserCRUDView.as_view()),
]