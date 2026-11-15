from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('reportes/', views.reportes, name='reportes'),

    path('habitaciones/', include('habitaciones.urls')),
    path('clientes/', include('clientes.urls')),
    path('reservaciones/', include('reservaciones.urls')),

    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
