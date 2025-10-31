from django import forms
from documentos.models import RegistroDocumento

TIPO_CHOICES = [
    ('documento', 'Documento'),
    ('contrato', 'Contrato'),
]


# Formulário sem campo de arquivo (será tratado separadamente)
class DocumentoUploadForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label="Tipo")

    class Meta:
        model = RegistroDocumento
        fields = ['tipo', 'titulo', 'descricao', 'data_emissao', 'data_vencimento']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = RegistroDocumento
        fields = ['titulo', 'descricao', 'data_emissao', 'data_vencimento']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
