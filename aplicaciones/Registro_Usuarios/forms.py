from django import forms
from .models import DatosTabla

class TiendaForm(forms.ModelForm):
    class Meta:
        model = DatosTabla
        fields = ['titulo', 'wr', 'tkr', 'abono', 'precio', 'peso_l', 'valor_peso']  # Excluir 'total_peso'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tienda'}),
            'wr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WR'}),
            'tkr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TKR'}),
            'abono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Abono'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'peso_l': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso (l)', 'step': '0.01'}),
            'valor_peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor/Peso', 'step': '0.01'}),
        }