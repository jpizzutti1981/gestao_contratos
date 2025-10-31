from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [

    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),

]