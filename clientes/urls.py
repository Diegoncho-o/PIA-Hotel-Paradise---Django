from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista'),
    path('nuevo/', views.crear_cliente, name='crear'),
    path('<int:pk>/editar/', views.editar_cliente, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar'),
]