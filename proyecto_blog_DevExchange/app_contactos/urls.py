from django.urls import path
from . import views
app_name = "app_contactos"
urlpatterns = [
    path("contacto/", views.ContactoUsuario.as_view(), name="contacto"),
]