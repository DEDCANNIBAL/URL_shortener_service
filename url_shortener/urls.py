from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='url_shortener'),
    re_path(r'(?P<short_url>[a-zA-Z0-9]+)', views.redirect_by_short_url, name='redirect')
]
