from django import forms
from .models import Comentario, Post, Etiqueta

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = { "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 8, "placeholder": "Escribe tu comentario aquí..."}) }

    

class CrearPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class NuevaEtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = '__all__'