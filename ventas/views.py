from django.shortcuts import render,redirect, get_object_or_404
from .models import Videojuego, Consola, Carrito, ElementoCarrito
from .forms import VideojuegoForm, ConsolaForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    
    else:
        form = VideojuegoForm()
    return render(request,'formulario_videojuegos.html',{'form':form})

def crear_consola(request):
    if request.method == 'POST':
        form = ConsolaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_consola')
        
    else:
        form = ConsolaForm()
    return render(request,'formulario_consola.html',{'form':form})

def lista_videojuegos(request, consola=None):
    if consola:
        videojuegos = Videojuego.objects.filter(id_consola=consola).order_by,('nom_juego')
    else:
        videojuegos = Videojuego.objects.all().order_by('id_consola','nom_juego')
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'lista_videojuegos.html', context)

def editar_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)

    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=videojuego)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    else:
        form = VideojuegoForm(instance=videojuego)

    return render(request, 'editar_videojuego.html',{'form':form})

def lista_inicio(request):
    videojuegos = Videojuego.objects.order_by('id_consola', 'nom_juego')
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'inicio.html', context)

def eliminar_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        videojuego.delete()
        return redirect('lista_videojuegos')
    return render(request, 'confirmar_eliminacion.html',{'videojuego':videojuego})

def lista_videojuegos_consola(request, consola):
    consola_obj = Consola.objects.get(nombre=consola)

    videojuegos = Videojuego.objects.filter(id_consola=consola_obj).order_by('nom_juego')

    context = {
        'videojuegos': videojuegos,
        'consola': consola,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'lista_videojuegos_consola.html', context)

def juego_detalle(request, juego_id):
    videojuego = get_object_or_404(Videojuego, pk=juego_id)
    juegos_recomendados = Videojuego.objects.filter(id_consola=videojuego.id_consola).exclude(pk=juego_id).order_by('?')[:2]

    context = {
        'videojuego': videojuego,
        'juegos_recomendados': juegos_recomendados,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'juego.html', context)

def buscar_juegos(request):
    query = request.GET.get('q','')
    juegos = Videojuego.objects.filter(nom_juego__icontains=query)
    context = {
        'query':query,
        'juegos': juegos,

    }
    return render(request, 'resultado_busqueda.html', context)

def nosotros(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'nosotros.html', context)

@login_required
def agregar_al_carrito(request, videojuego_id):
    videojuego = get_object_or_404(Videojuego, id_producto = videojuego_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elemento_carrito, creado = ElementoCarrito.objects.get_or_create(
        carrito=carrito, videojuego=videojuego, defaults={'precio': videojuego.precio}
    )

    if not creado:
        elemento_carrito.cantidad +=1
        elemento_carrito.save()

    return redirect('ver_carrito')
@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elementos_carrito = ElementoCarrito.objects.filter(carrito=carrito)
    total_precio = sum(item.precio * item.cantidad for item in elementos_carrito)
    iva = total_precio * 0.19
    subtotal = total_precio - iva
    context = {
        'elementos_carrito': elementos_carrito,
        'total_precio': total_precio,
        'iva':iva,
        'subtotal':subtotal,
    }
    return render(request, 'carrito.html', context)

@login_required
def eliminar_del_carrito(request, elemento_carrito_id):
    elemento_carrito = get_object_or_404(ElementoCarrito, id=elemento_carrito_id)
    elemento_carrito.delete()
    return redirect('ver_carrito')