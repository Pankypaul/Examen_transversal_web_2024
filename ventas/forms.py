from django import forms
from .models import Videojuego, Consola, Comuna
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }
        help_texts = {
            'password1': _("<br>Tu contraseña no puede ser demasiado similar a tu otra información personal.<br>"
                           "Tu contraseña debe contener al menos 8 caracteres.<br>"
                           "Tu contraseña no puede ser una contraseña común.<br>"
                           "Tu contraseña no puede ser completamente numérica."),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].validators = []
        self.fields['password1'].help_text = self.Meta.help_texts['password1']

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

class AutentificacionForm(AuthenticationForm):
    username = forms.CharField(label=_('Correo electrónico'), max_length=256)

    error_messages = {
        'invalid_login': _(
            "Por favor, introduzca un %(username) válido y una contraseña correcta."
            "Tenga en cuenta que las mayúsculas y minúsculas se consideran diferentes."
        ),
        'inactive': _("Tu cuenta está inactiva."),
    }