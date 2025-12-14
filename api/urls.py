from django.urls import path, include
from rest_framework import routers
from .views import (
    health,
    info,
    EdificioViewSet,
    DepartamentoViewSet,
    SensorViewSet,
    EventoViewSet,
    BarreraViewSet
)

router = routers.DefaultRouter()
router.register(r'edificios', EdificioViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'barrera', BarreraViewSet)

urlpatterns = [
    path('health/', health),
    path('info/', info),
    path('', include(router.urls)),
]
