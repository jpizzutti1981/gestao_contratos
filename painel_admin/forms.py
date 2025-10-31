from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from usuarios.models import Usuario
from documentos.models import Shopping

class ShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = ['nome', 'sigla', 'cnpj', 'email_alertas']

class UsuarioForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        required=False        
    )
    shopping = forms.ModelChoiceField(
        queryset=Shopping.objects.all(),
        label="Shopping",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2', 'grupo', 'shopping'
        ]

class UsuarioEditForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    shopping = forms.ModelChoiceField(
        queryset=Shopping.objects.all(),
        label="Shopping",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Usuario  # <-- use seu modelo customizado
        fields = ['username', 'email', 'first_name', 'last_name', 'grupo', 'shopping']

from django import forms
from usuarios.models import Usuario, Perfil
from documentos.models import Shopping

class PerfilForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Usuário", widget=forms.Select(attrs={'class': 'form-select'}))
    shopping = forms.ModelChoiceField(queryset=Shopping.objects.all(), label="Shopping", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Perfil
        fields = ['usuario', 'shopping']