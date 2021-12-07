from django.contrib import admin
# Register your models here.
from .models import User, Paquete, CompraPaquete, Vehiculo, TipoVehiculo, Parqueo, DetalleParqueo

admin.site.register(User)
admin.site.register(Paquete)
admin.site.register(CompraPaquete)
admin.site.register(Vehiculo)
admin.site.register(TipoVehiculo)
admin.site.register(Parqueo)
admin.site.register(DetalleParqueo)
