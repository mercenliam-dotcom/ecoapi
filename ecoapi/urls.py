from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN JWT
    path('login_jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_jwt/', TokenRefreshView.as_view(), name='token_refresh'),

    # API PRINCIPAL
    path('api/', include('api.urls')),
]

from django.conf.urls import handler404

def error_404(request, exception=None):
    from django.http import JsonResponse
    return JsonResponse(
        {"error": "La ruta solicitada no existe."},
        status=404
    )

handler404 = error_404

from django.conf.urls import handler500

def error_500(request):
    from django.http import JsonResponse
    return JsonResponse(
        {"error": "Error interno del servidor."},
        status=500
    )

handler500 = error_500
