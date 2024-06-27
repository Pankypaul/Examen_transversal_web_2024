from django.urls import path
from . import views

urlpatterns = [    
    path('nav', views.nav, name="nav"),
    path('footer', views.footer, name="footer"),
    path('base', views.base, name="base")
]