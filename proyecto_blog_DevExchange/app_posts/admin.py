from django.contrib import admin

# Register your models here.
from .models import  Post, Etiqueta, Voto, Comentario


admin.site.register(Post)
admin.site.register(Etiqueta)
admin.site.register(Voto)
admin.site.register(Comentario)