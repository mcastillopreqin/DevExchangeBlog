from django.urls import path
from . import views

urlpatterns = [
   path("", views.inicio , name="inicio"), 
   path("", views.lista_posts, name="lista_posts"),
   path("<int:post_id>/", views.detalle_post, name="detalle_post"),
   path('<int:post_id>/voto/<int:tipo_voto>/', views.voto_post, name='voto_post'),
]