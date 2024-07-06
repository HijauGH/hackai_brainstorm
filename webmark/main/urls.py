from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name='home'),
    path('api/', views.api_handler, name='api')
]
