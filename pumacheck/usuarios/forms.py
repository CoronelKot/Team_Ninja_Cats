from django import forms
from usuarios.models import Usuario
import re

class CrearCuentaForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    apellidos = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=15, required=True)
    correo = forms.EmailField(required=True)
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput, required=True)
    campus = forms.IntegerField(required=True)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) <= 2:
            raise forms.ValidationError("El nombre debe tener 3 o más caracteres.")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if len(apellidos) <= 2:
            raise forms.ValidationError("Los apellidos deben tener 3 o más caracteres.")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellidos):
            raise forms.ValidationError("Los apellidos solo pueden contener letras y espacios.")
        return apellidos
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) <= 9:
            raise forms.ValidationError("El número debe tener 10 dígitos.")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        telefono = cleaned_data.get('telefono')
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")

        # Verificar si el teléfono ya está registrado
        if Usuario.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError("El número de teléfono ya está registrado.")

        # Verificar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
    