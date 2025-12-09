from django.contrib import admin

# Register your models here.
from .models import  Post, Etiqueta, Voto, Comentario


admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estado', 'fecha_publicacion')
    list_filter = ('estado', 'fecha_publicacion', 'autor')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    
admin.site.register(Etiqueta)
admin.site.register(Voto)
admin.site.register(Comentario)