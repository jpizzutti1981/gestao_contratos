from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.models import Group
from documentos.models import Shopping

class UsuarioCreationForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        required=True  # ✅ agora é obrigatório
    )
    shopping = forms.ModelChoiceField(
        queryset=Shopping.objects.all(),
        label="Shopping",
        required=False
    )
    is_superuser = forms.BooleanField(
        label="É Superusuário?",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2', 'grupo', 'shopping', 'is_superuser'
        )
