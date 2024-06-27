from django.shortcuts import render,redirect, get_object_or_404
from .models import Videojuego, Consola
from . forms import VideojuegoForm, ConsolaForm
from django.conf import settings

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