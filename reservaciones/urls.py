from django.urls import path
from . import views

app_name = 'reservaciones'

urlpatterns = [
    path('', views.lista_reservaciones, name='lista'),
    path('nuevo/', views.crear_reservacion, name='crear'),
    path('disponibilidad/', views.consultar_disponibilidad, name='disponibilidad'),
    path('<int:pk>/editar/', views.editar_reservacion, name='editar'),
    path('<int:pk>/cancelar/', views.cancelar_reservacion, name='cancelar'),
]