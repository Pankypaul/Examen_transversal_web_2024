from django.forms import ValidationError
from django.shortcuts import render,redirect, get_object_or_404
from .models import Videojuego, Consola, Carrito, ElementoCarrito, Compra
from .forms import VideojuegoForm, ConsolaForm,ComunaForm, RegistroUsuarioForm, AutentificacionForm, ResetPasswordForm, CambiarContrasenaForm, DetallesPagoForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
import ssl
import smtplib
from email.message import EmailMessage
from django.contrib.auth.models import User
from django.template.defaultfilters import floatformat

def crear_consola(request):
    if request.method == 'POST':
        form = ConsolaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_consola')
        
    else:
        form = ConsolaForm()
    return render(request,'formulario_consola.html',{'form':form})
def crear_comuna(request):
    if request.method == 'POST':
        form = ComunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inicio')
    else:
        form = ComunaForm()
    
    context = {
        'form': form,
    }
    return render(request, 'crear_comuna.html',context)

def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    
    else:
        form = VideojuegoForm()
    return render(request,'formulario_videojuegos.html',{'form':form})

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

def eliminar_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        videojuego.delete()
        return redirect('lista_videojuegos')
    return render(request, 'confirmar_eliminacion.html',{'videojuego':videojuego})

def lista_inicio(request):
    videojuegos = Videojuego.objects.order_by('id_consola', 'nom_juego')
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'inicio.html', context)

def redireccion_juegos(request, consola=None):
    if request.user.is_authenticated and request.user.is_staff:
        videojuegos = Videojuego.objects.filter(id_consola=consola).order_by('nom_juego') if consola else Videojuego.objects.all().order_by('id_consola', 'nom_juego')
        template = 'lista_videojuegos_staff.html'
    else:
        videojuegos = Videojuego.objects.filter(id_consola=consola).order_by('nom_juego') if consola else Videojuego.objects.all().order_by('id_consola', 'nom_juego')
        template = 'lista_videojuegos.html'

    context = {
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, template, context)

def redireccionar_consola(request, consola):
    consola_obj = Consola.objects.get(nombre=consola)
    videojuegos = Videojuego.objects.filter(id_consola=consola_obj).order_by('nom_juego')
    if request.user.is_authenticated and request.user.is_staff:
        template = 'lista_videojuegos_consola_staff.html'

    else:
        template = 'lista_videojuegos_consola.html'

    context = {
        'videojuegos': videojuegos,
        'consola': consola,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, template, context)

def juego_detalle(request, juego_id):
    videojuego = get_object_or_404(Videojuego, pk=juego_id)
    juegos_recomendados = Videojuego.objects.filter(id_consola=videojuego.id_consola).exclude(pk=juego_id).order_by('?')[:2]

    precio_formateado = "{:,.0f}".format(videojuego.precio)
    precio_formateado = precio_formateado.replace(',', '.')

    context = {
        'videojuego': videojuego,
        'juegos_recomendados': juegos_recomendados,
        'precio_formateado': precio_formateado,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'juego.html', context)

def redireccion_buscar(request):
    if request.user.is_authenticated and request.user.is_staff:
        query = request.GET.get('q','')
        juegos = Videojuego.objects.filter(nom_juego__icontains=query)
        template = 'resultado_busqueda_staff.html'

    else:
        query = request.GET.get('q','')
        juegos = Videojuego.objects.filter(nom_juego__icontains=query)
        template ='resultado_busqueda.html'
    context = {
        'query':query,
        'juegos': juegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, template, context)

def nosotros(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'nosotros.html', context)

@login_required
def agregar_al_carrito(request, videojuego_id):
    if request.method == 'POST':
        videojuego = get_object_or_404(Videojuego, id_producto=videojuego_id)
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

        cantidad = int(request.POST.get('cantidad', 1))

        elemento_carrito = ElementoCarrito.objects.filter(carrito=carrito, videojuego=videojuego).first()

        if elemento_carrito is None:
            elemento_carrito = ElementoCarrito.objects.create(
                carrito=carrito, videojuego=videojuego, precio=videojuego.precio, cantidad=cantidad
            )
        else:
            elemento_carrito.cantidad = cantidad
            elemento_carrito.save()

        return redirect('ver_carrito')
    
    return redirect('juego_detalle', videojuego_id=videojuego_id)
    
@login_required(login_url='accounts/login/')
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elementos_carrito = ElementoCarrito.objects.filter(carrito=carrito)
    total_precio = sum(item.precio * item.cantidad for item in elementos_carrito)

    precio_formateado = "{:,.0f}".format(total_precio)
    precio_formateado = precio_formateado.replace(',', '.')

    iva_formateado = "{:,.0f}".format(iva)
    iva_formateado = iva_formateado.replace(',', '.')

    subtotal_formateado = "{:,.0f}".format(subtotal)
    subtotal_formateado = subtotal_formateado.replace(',', '.')

    iva = total_precio * 0.19
    subtotal = total_precio - iva
    context = {
        'elementos_carrito': elementos_carrito,
        'precio_formateado': precio_formateado,
        'iva_formateado': iva_formateado,
        'subtotal_formateado': subtotal_formateado,
        'MEDIA_URL': settings.MEDIA_URL,

    }
    return render(request, 'carrito.html', context)

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Necesita iniciar sesión para entrar al carrito')
            return redirect('/accounts/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

@custom_login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elementos_carrito = ElementoCarrito.objects.filter(carrito=carrito)
    total_precio = sum(item.precio * item.cantidad for item in elementos_carrito)
    iva = total_precio * 0.19
    subtotal = total_precio - iva

    precio_formateado = "{:,.0f}".format(total_precio)
    precio_formateado = precio_formateado.replace(',', '.')

    iva_formateado = "{:,.0f}".format(iva)
    iva_formateado = iva_formateado.replace(',', '.')

    subtotal_formateado = "{:,.0f}".format(subtotal)
    subtotal_formateado = subtotal_formateado.replace(',', '.')
    context = {
        'elementos_carrito': elementos_carrito,
        'precio_formateado': precio_formateado,
        'iva_formateado': iva_formateado,
        'subtotal_formateado': subtotal_formateado,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'carrito.html', context)

@login_required
def eliminar_del_carrito(request, elemento_carrito_id):
    elemento_carrito = get_object_or_404(ElementoCarrito, id=elemento_carrito_id)
    elemento_carrito.delete()
    return redirect('ver_carrito')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inicio')
    else:
        form = RegistroUsuarioForm()
    context = {
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'registrar.html', context)

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AutentificacionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_inicio')
    else:
        form = AutentificacionForm()
    return render(request,'registration/login.html',{'form': form})

@login_required
def confirmar_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logged_out')
    return render(request, 'registration/confirm_logout.html')

def resetear_contrasena(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                token = account_activation_token.make_token(usuario)
                uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

                # Crear el mensaje de correo
                subject = 'Restablecimiento de contraseña'
                body = render_to_string('password_reset_email.html', {
                    'user': usuario,
                    'url': url,
                })
                
                email = 'megagames185@gmail.com'
                contrasena = 'gnlcnnkxuajkwnjp'
                destinatario = usuario.username

                # Crear objeto de mail
                em = EmailMessage()
                em['From'] = email
                em['To'] = destinatario
                em['Subject'] = subject
                em.set_content(body)

                # Añadir SSL (extra de seguridad)
                context = ssl.create_default_context()

                # Iniciar sesión y enviar el mail
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email, contrasena)
                    smtp.sendmail(email, destinatario, em.as_string())

                return redirect('lista_inicio')  # Cambia esto según sea necesario
            except ValidationError as e:
                form.add_error('email', e)
                pass
    else:
        form = ResetPasswordForm()

    return render(request, 'resetear_contrasena.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = CambiarContrasenaForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('lista_inicio')
        else:
            form = CambiarContrasenaForm()
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')

def eliminar_juego_carrito(request, item_id):
    if request.method == 'POST':
        elemento = get_object_or_404(ElementoCarrito, id=item_id)
        elemento.delete()
        return redirect('ver_carrito')
    return redirect('lista_inicio')
@require_POST
def  actualizar_cantidad_carrito(request, elemento_carrito_id):
    elemento_carrito = get_object_or_404(ElementoCarrito, id=elemento_carrito_id)
    carrito = elemento_carrito.carrito

    action = request.POST.get('action')

    if action == 'remove':
        if elemento_carrito.cantidad > 1:
            elemento_carrito.cantidad -= 1
            elemento_carrito.save()
    elif action == 'add':
        if elemento_carrito.cantidad < elemento_carrito.videojuego.stock_juego:
            elemento_carrito.cantidad += 1
            elemento_carrito.save()

    return redirect('ver_carrito')

def obtener_carrito_usuario(usuario):
    try:
        carrito = Carrito.objects.get(usuario=usuario)
    except Carrito.DoesNotExist:
        carrito = Carrito(usuario=usuario)
        carrito.save()
    return carrito

def pagar(request):
    if request.method == 'POST':
        form = DetallesPagoForm(request.POST)
        if form.is_valid():
            detalles_pago = form.save(commit=False)
            detalles_pago.usuario = request.user

            carrito = obtener_carrito_usuario(request.user)
            if carrito:
                for item in ElementoCarrito.objects.filter(carrito=carrito):
                    compra = Compra(
                        usuario=request.user,
                        videojuego=item.videojuego,
                        cantidad=item.cantidad,
                        direccion_envio=detalles_pago.direccion_envio
                    )
                    compra.save()

                carrito.elementocarrito_set.all().delete()
                carrito.delete()

            return redirect('lista_inicio')
    else:
        form = DetallesPagoForm()

    return render(request, 'pagar.html', {'form': form})