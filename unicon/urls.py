from django.urls import path
from . import views
from django.conf.urls import include,url
from django.conf import settings

urlpatterns = [
  path('sign_up', views.SaveCustomer.as_view(), name='sign_up'),
  path('auth', views.Authenticate.as_view(), name='auth'),
  
]
