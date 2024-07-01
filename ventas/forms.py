from django import forms
from .models import Videojuego, Consola, Comuna
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

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

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data['email']
        try:
            usuario = User.objects.get(username=email)
            return usuario
        except User.DoesNotExist:
            raise ValidationError("No hay ninguna cuenta asociada a ese correo electrónico.")


class CambiarContrasenaForm(forms.Form):
    password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
    



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()