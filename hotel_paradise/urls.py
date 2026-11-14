
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('habitaciones/', include('habitaciones.urls')),
    path('clientes/', include('clientes.urls')),
    path('reservaciones/', include('reservaciones.urls')),

    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
