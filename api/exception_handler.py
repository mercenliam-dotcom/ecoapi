from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Si DRF ya generó una respuesta, la modificamos
    if response is not None:

        # Error 400 - Validación
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(
                {"error": "Datos inválidos", "detalles": response.data},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Error 401 - No autenticado
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"error": "No autenticado. Token JWT requerido."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Error 403 - No permitido
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response(
                {"error": "No tienes permisos para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Error 404 - Objeto no encontrado
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return Response(
                {"error": "El recurso solicitado no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

    # Errores que Django no manejó → 500
    return Response(
        {"error": "Error interno del servidor."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
