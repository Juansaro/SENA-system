from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )


class CargarAprendicesForm(forms.Form):
    archivo_excel = forms.FileField(
        required=True,
        label="Seleccione el archivo Excel",
        widget=forms.FileInput(attrs={"accept": ".xlsx"}),
    )

