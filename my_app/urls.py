from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("perfil", views.perfil_view, name="perfil"),
    path("crear_paquete", views.crear_paquete_view, name="crear_paquete"),
    path("paquetes", views.paquetes_view, name="paquetes"),
    path("registrar_vehiculo", views.registrar_vehiculo_view, name="registrar_vehiculo"),
    path("mis_vehiculos", views.mis_vehiculos_view, name="mis_vehiculos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)