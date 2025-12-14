from rest_framework import serializers
from .models import (
    Edificio, UserProfile, Departamento,
    Sensor, Barrera, Evento
)
from django.contrib.auth.models import User


class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = "__all__"


class DepartamentoSerializer(serializers.ModelSerializer):
    edificio_nombre = serializers.CharField(source="edificio.nombre", read_only=True)
    operador_nombre = serializers.CharField(source="operador.username", read_only=True)

    class Meta:
        model = Departamento
        fields = "__all__"

    def validate(self, data):
        request = self.context.get("request")
        user = request.user

        perfil = UserProfile.objects.filter(user=user).first()
        if not perfil:
            raise serializers.ValidationError("El usuario no tiene perfil asociado.")

        # Validación principal: dominio por edificio
        if perfil.rol == "ADMIN":
            if data["edificio"] != perfil.edificio:
                raise serializers.ValidationError(
                    "No puedes crear departamentos en otro edificio."
                )

            operador = data["operador"]
            operador_perfil = UserProfile.objects.filter(user=operador).first()
            if not operador_perfil or operador_perfil.edificio != perfil.edificio:
                raise serializers.ValidationError(
                    "No puedes asignar un operador de otro edificio."
                )

        return data


class SensorSerializer(serializers.ModelSerializer):
    departamento_numero = serializers.CharField(source="departamento.numero", read_only=True)

    class Meta:
        model = Sensor
        fields = "__all__"

    def validate_uid(self, value):
        if Sensor.objects.filter(uid=value).exists():
            raise serializers.ValidationError("El UID del sensor ya está registrado.")
        return value

    def validate(self, data):
        request = self.context.get("request")
        perfil = UserProfile.objects.filter(user=request.user).first()

        if perfil and perfil.rol == "ADMIN":
            if data["departamento"].edificio != perfil.edificio:
                raise serializers.ValidationError(
                    "No puedes registrar sensores en otro edificio."
                )
        return data


class BarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrera
        fields = "__all__"

    def validate(self, data):
        request = self.context.get("request")
        perfil = UserProfile.objects.filter(user=request.user).first()

        if perfil and perfil.rol == "ADMIN":
            if data["departamento"].edificio != perfil.edificio:
                raise serializers.ValidationError(
                    "No puedes gestionar barreras de otro edificio."
                )
        return data


class EventoSerializer(serializers.ModelSerializer):
    sensor_uid = serializers.CharField(source="sensor.uid", read_only=True)

    class Meta:
        model = Evento
        fields = "__all__"
        read_only_fields = ["fecha"]

    def validate(self, data):
        if not data.get("sensor") and not data.get("barrera"):
            raise serializers.ValidationError(
                "El evento debe estar asociado a un sensor o a una barrera."
            )
        return data
