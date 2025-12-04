from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import  Post, Etiqueta, Voto, Comentario

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'nombredeusuario', 'ubicacion', 'fecha_nac', 'is_staff']
#     fieldsets = UserAdmin.fieldsets + (
#         ('Información Adicional', {'fields': ('bio', 'ubicacion', 'fecha_nac')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ('Información Adicional', {'fields': ('bio', 'ubicacion', 'fecha_nac')}),
#     )

#admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Etiqueta)
admin.site.register(Voto)
admin.site.register(Comentario)