from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name='home'),
<<<<<<< HEAD
    path('/', views.api_handler, name='api')
=======
>>>>>>> e7c2fac (server v0.2)
]
