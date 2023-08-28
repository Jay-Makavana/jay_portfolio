from . import views
from django.urls import path, include
from .views import *
app_name='portfolio_app'

urlpatterns = [
      path('',home_view.as_view(), name="home_view")
]