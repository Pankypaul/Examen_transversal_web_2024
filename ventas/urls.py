from django.urls import path
from . import views
from .views import agregar_al_carrito, ver_carrito, eliminar_del_carrito
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('videojuegos/nuevo', views.crear_videojuego, name='crear_videojuego'),
    path('videojuegos/nueva_consola', views.crear_consola, name='crear_consola'),
    path('videojuegos/', views.redireccion_juegos, name='lista_videojuegos'),
    path('videojuegos/editar/<int:pk>/', views.editar_videojuego, name='editar_videojuego'),
    path('', views.lista_inicio, name='lista_inicio'),
    path('videojuegos/eliminar/<int:pk>/', views.eliminar_videojuego, name='eliminar_videojuego'),
    path('videojuegos/<str:consola>/', views.lista_videojuegos_consola, name='lista_videojuegos_consola'),
    path('videojuego/<int:juego_id>/', views.juego_detalle, name='juego_detalle'),
    path('buscar/', views.buscar_juegos, name='buscar_juegos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('agregar_carrito/<int:videojuego_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<int:elemento_carrito_id>', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('nueva_comuna/', views.crear_comuna, name='crear_comuna'),
    path('ingresar', views.iniciar_sesion, name='ingresar'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
]