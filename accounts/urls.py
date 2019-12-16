from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterFormView.as_view(), name='sign_up'),
    path('login/', views.LoginFormView.as_view(), name='sign_in'),
    path('logout/', views.LogoutView.as_view(), name='sign_out'),
]
