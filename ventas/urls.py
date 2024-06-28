from django.urls import path
from . import views

urlpatterns = [
    path('videojuegos/nuevo', views.crear_videojuego, name='crear_videojuego'),
    path('videojuegos/nueva_consola', views.crear_consola, name='crear_consola'),
    path('videojuegos/', views.lista_videojuegos, name='lista_videojuegos'),
    path('videojuegos/editar/<int:pk>/', views.editar_videojuego, name='editar_videojuego'),
    path('', views.lista_inicio, name='lista_inicio'),
    path('videojuegos/eliminar/<int:pk>/', views.eliminar_videojuego, name='eliminar_videojuego'),
    path('videojuegos/<str:consola>/', views.lista_videojuegos_consola, name='lista_videojuegos_consola'),
    path('videojuego/<int:juego_id>/', views.juego_detalle, name='juego_detalle'),
    path('buscar/', views.buscar_juegos, name='buscar_juegos'),
    path('nosotros/', views.nosotros, name='nosotros')
]