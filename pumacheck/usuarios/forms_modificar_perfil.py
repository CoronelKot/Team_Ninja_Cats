from django import forms
from usuarios.models import Usuario
import re

class ModificarPerfilForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100, required=False)
    telefono = forms.CharField(max_length=15, required=False)
    correo = forms.EmailField(required=False)
    campus = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) <= 2:
            raise forms.ValidationError("El nombre debe tener 3 o más caracteres.")
        if nombre and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if apellidos and len(apellidos) <= 2:
            raise forms.ValidationError("Los apellidos deben tener 3 o más caracteres.")
        if apellidos and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellidos):
            raise forms.ValidationError("Los apellidos solo pueden contener letras y espacios.")
        return apellidos

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and len(telefono) != 10:
            raise forms.ValidationError("El número debe tener 10 dígitos.")
        if not telefono or telefono == self.usuario_actual.telefono:
            return telefono

        # Validar que no exista otro usuario con este correo
        if Usuario.objects.filter(telefono=telefono).exclude(id=self.usuario_actual.id).exists():
            raise forms.ValidationError("El teléfono ya está registrado.")
    
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        # Comparar explícitamente con el correo actual
        if not correo or correo == self.usuario_actual.correo:
            return correo 

        if Usuario.objects.filter(correo=correo).exclude(id=self.usuario_actual.id).exists():
            raise forms.ValidationError("El correo ya está registrado.")

        return correo

    def clean(self):
        cleaned_data = super().clean()
        # Solo realiza validaciones adicionales si es necesario
        return cleaned_data
