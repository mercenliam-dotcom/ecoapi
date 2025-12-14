from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

from .models import (
    Edificio, Departamento, Sensor,
    Evento, Barrera, UserProfile
)
from .serializers import (
    EdificioSerializer, DepartamentoSerializer,
    SensorSerializer, EventoSerializer,
    BarreraSerializer
)

# -----------------------------
#     ENDPOINT PUBLICO INFO
# -----------------------------
@api_view(["GET"])
def info(request):
    data = {
        "autor": "Felipe Martinez",
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect",
        "descripcion": "API REST para control de acceso con sensores RFID y barrera",
        "version": "1.0"
    }
    return Response(data)


# -----------------------------
#         HEALTH CHECK
# -----------------------------
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


# -----------------------------
#     PERMISOS PERSONALIZADOS
# -----------------------------
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    ADMIN     -> CRUD completo
    OPERADOR  -> Solo lectura
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        profile = UserProfile.objects.filter(user=request.user).first()
        return profile and profile.rol == "ADMIN"


# -----------------------------
#        VIEWSETS CRUD
# -----------------------------
class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class BarreraViewSet(viewsets.ModelViewSet):
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
