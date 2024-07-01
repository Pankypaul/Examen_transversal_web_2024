from django.db import models
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    return os.path.join('pagina', filename)

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Consola(models.Model):
    id_consola = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_juego = models.CharField(max_length=100)
    stock_juego = models.IntegerField()
    descripcion = models.TextField()
    image = models.ImageField(upload_to=get_image_path)
    precio = models.IntegerField()
    id_consola = models.ForeignKey(Consola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_juego

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    direccion_envio = models.TextField()

    def __str__(self):
        return f"Compra #{self.id_compra} - Usuario: {self.usuario.username}, Producto: {self.videojuego.nom_juego}"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(User, related_name='carritos', on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    def vaciar_carrito(self):
        self.elementocarrito_set.all().delete()
        self.delete()

class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.IntegerField()