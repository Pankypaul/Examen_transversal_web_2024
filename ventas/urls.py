from django.urls import path
from . import views
from .views import agregar_al_carrito, ver_carrito, eliminar_del_carrito, confirmar_logout, resetear_contrasena, password_reset_confirm
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.lista_inicio, name='lista_inicio'),
    path('videojuegos/', views.redireccion_juegos, name='lista_videojuegos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('videojuegos/nuevo', views.crear_videojuego, name='crear_videojuego'),
    path('videojuegos/nueva_consola', views.crear_consola, name='crear_consola'),
    path('videojuegos/editar/<int:pk>/', views.editar_videojuego, name='editar_videojuego'),
    path('videojuegos/eliminar/<int:pk>/', views.eliminar_videojuego, name='eliminar_videojuego'),
    path('videojuegos/<str:consola>/', views.redireccionar_consola, name='lista_videojuegos_consola'),
    path('videojuego/<int:juego_id>/', views.juego_detalle, name='juego_detalle'),
    path('buscar/', views.redireccion_buscar, name='buscar_juegos'),
    path('agregar_carrito/<int:videojuego_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<int:elemento_carrito_id>', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('nueva_comuna/', views.crear_comuna, name='crear_comuna'),
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('accounts/confirm_logout/', views.confirmar_logout, name='confirm_logout'),
    path('accounts/logout/', TemplateView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
    path('resetear_contrasena/', views.resetear_contrasena, name='resetear_contrasena'),
    path('resetear_contrasena/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('eliminar/<int:item_id>/', views.eliminar_juego_carrito, name='eliminar_juego_carrito'),
    path('actualizar_cantidad_carrito/<int:elemento_carrito_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('pagar/', views.pagar, name='pagar'),
    ]