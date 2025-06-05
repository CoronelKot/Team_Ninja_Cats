from django import forms
from usuarios.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'telefono', 'correo']

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        usuario_id = self.instance.id if self.instance else None
        if Usuario.objects.exclude(id=usuario_id).filter(correo=correo).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        usuario_id = self.instance.id if self.instance else None
        if Usuario.objects.exclude(id=usuario_id).filter(telefono=telefono).exists():
            raise forms.ValidationError("Este teléfono ya está en uso.")
        return telefono

    