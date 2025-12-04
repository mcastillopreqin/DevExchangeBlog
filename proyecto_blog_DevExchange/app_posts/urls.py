from django.urls import path
from . import views

urlpatterns = [
   path("posts/", views.lista_posts, name="lista_posts"),
   path("post/<int:post_id>/", views.detalle_post, name="detalle_post"),
   path('post/<int:post_id>/voto/<int:tipo_voto>/', views.voto_post, name='voto_post'),
]