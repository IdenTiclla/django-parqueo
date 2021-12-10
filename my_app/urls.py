from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("perfil", views.perfil_view, name="perfil"),
    path("crear_paquete", views.crear_paquete_view, name="crear_paquete"),
    path("paquetes", views.paquetes_view, name="paquetes"),
]