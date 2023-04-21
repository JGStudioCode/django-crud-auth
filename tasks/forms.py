# Formulario de tareas
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task #desde que modelo usar
        fields = ['title', 'description', 'important'] #campos del modelo
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a titile'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Write a description'}),
            'important' : forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
