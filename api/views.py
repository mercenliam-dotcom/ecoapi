from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    return Response({
        "autor": "Felipe Martinez",
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect",
        "version": "1.0"
    })


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


# -----------------------------
#     PERMISOS
# -----------------------------
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        perfil = UserProfile.objects.filter(user=request.user).first()
        return perfil and perfil.rol == "ADMIN"


# -----------------------------
#        VIEWSETS
# -----------------------------
class BaseDestroyMessageViewSet(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"mensaje": "Eliminado correctamente"},
            status=status.HTTP_200_OK
        )


class EdificioViewSet(BaseDestroyMessageViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [IsAdminOrReadOnly]


class DepartamentoViewSet(BaseDestroyMessageViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly]


class SensorViewSet(BaseDestroyMessageViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]


class BarreraViewSet(BaseDestroyMessageViewSet):
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAdminOrReadOnly]


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]
