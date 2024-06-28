from django import forms
from .models import Videojuego, Consola, Comuna, Usuario

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['nom_juego','stock_juego', 'descripcion', 'image', 'precio', 'id_consola']

class ConsolaForm(forms.ModelForm):
    class Meta:
        model = Consola
        fields = ['nombre']

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['nom_juego','stock_juego', 'descripcion', 'image', 'precio', 'id_consola']

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ['nombre']

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'a_paterno', 'a_materno', 'direccion', 'email1', 'cel1', 'password','id_comuna']
    id_comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(),empty_label="Selecciona una comuna")