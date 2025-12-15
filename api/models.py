from django.db import models
from django.contrib.auth.models import User


# -------------------------
#  EDIFICIOS
# -------------------------
class Edificio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


# -------------------------
#  PERFIL DE USUARIO
# -------------------------
class UserProfile(models.Model):
    ROLES = [
        ("ADMIN", "Administrador"),
        ("OPERADOR", "Operador"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


# -------------------------
#  DEPARTAMENTOS
# -------------------------
class Departamento(models.Model):
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)

    planta = models.IntegerField()
    numero = models.CharField(max_length=10)


    def __str__(self):
        return f"{self.edificio.nombre} - {self.numero} (Planta {self.planta})"


# -------------------------
#  SENSORES RFID
# -------------------------
class Sensor(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
        ("bloqueado", "Bloqueado"),
        ("perdido", "Perdido"),
    ]

    TIPOS = [
        ("llavero", "Llavero"),
        ("tarjeta", "Tarjeta"),
    ]

    uid = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uid} ({self.tipo})"


# -------------------------
#  BARRERA
# -------------------------
class Barrera(models.Model):
    departamento = models.OneToOneField(Departamento, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=10,
        choices=[("abierta", "Abierta"), ("cerrada", "Cerrada")],
        default="cerrada"
    )
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Barrera {self.departamento.numero} - {self.estado}"


# -------------------------
#  EVENTOS
# -------------------------
class Evento(models.Model):
    TIPOS = [
        ("RFID", "Acceso RFID"),
        ("BARRERA", "Apertura Barrera"),
    ]

    RESULTADOS = [
        ("permitido", "Permitido"),
        ("denegado", "Denegado"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    resultado = models.CharField(max_length=20, choices=RESULTADOS)

    sensor = models.ForeignKey(
        Sensor, null=True, blank=True, on_delete=models.SET_NULL
    )
    barrera = models.ForeignKey(
        Barrera, null=True, blank=True, on_delete=models.SET_NULL
    )

    usuario = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.resultado} - {self.fecha}"
