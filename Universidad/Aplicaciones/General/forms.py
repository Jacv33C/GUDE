from django import forms
from .models import HistorialAcademico

class HistorialForm(forms.ModelForm):
    class Meta:
        model = HistorialAcademico
        fields = ['alumno', 'curso', 'calificacion', 'fecha']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
