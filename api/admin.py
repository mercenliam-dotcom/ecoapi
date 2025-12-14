from django.contrib import admin
from .models import (
    Edificio,
    UserProfile,
    Departamento,
    Sensor,
    Barrera,
    Evento
)

admin.site.register(Edificio)
admin.site.register(UserProfile)
admin.site.register(Departamento)
admin.site.register(Sensor)
admin.site.register(Barrera)
admin.site.register(Evento)
