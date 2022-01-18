from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # urls para usuarios
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("perfil", views.perfil_view, name="perfil"),
    
    path("registrar_vehiculo", views.registrar_vehiculo_view, name="registrar_vehiculo"),
    path("mis_vehiculos", views.mis_vehiculos_view, name="mis_vehiculos"),
    path("comprar_paquetes", views.comprar_paquetes_view, name="comprar_paquetes"),
    path("comprar/<int:id>", views.comprar_view, name="comprar"),
    path("mis_suscripciones", views.mis_suscripciones_view, name="mis_suscripciones"),
    path("parqueo", views.parqueo_view, name="parqueo"),
    path("parquear/<int:id>", views.parquear_view, name="parquear"),

    # urls para administradores
    path("crear_paquete", views.crear_paquete_view, name="crear_paquete"),
    path("paquetes", views.paquetes_view, name="paquetes"),
    path("activaciones", views.activaciones_view, name="activaciones"),
    path("activar/<int:id>", views.activar_view, name="activar"),
    path("crear_parqueo", views.crear_parqueo_view, name="crear_parqueo"),
    path("mis_parqueos", views.mis_parqueos_view, name="mis_parqueos"),
    path("suscripciones_vencidas", views.suscripciones_vencidas_view, name="suscripciones_vencidas"),
    path("desactivar/<int:id>", views.desactivar_view, name="desactivar"),
    # urls para guardias
    path("marcar_salidas", views.marcar_salidas_view, name="marcar_salidas"),
    path("marcar_salida/<int:id>", views.marcar_salida_view, name="marcar_salida"),
    path("ver_salidas", views.ver_salidas_view, name="ver_salidas"),
    # urls para contabilidad
    path("reportes_suscripciones_compradas", views.reportes_suscripciones_compradas_view, name="reportes_suscripciones_compradas"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)