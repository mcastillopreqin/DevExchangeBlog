from django.urls import path
from . import views
from .views import registro_view, login_view, logout_view

urlpatterns = [
    path("registro/", registro_view, name="registro"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('usuarios/', views.UsuarioListView.as_view(), name='lista_usuarios'),
    path('eliminar_usuario/<int:pk>/', views.UsuarioDeleteView.as_view(), name='eliminar_usuario'),
]