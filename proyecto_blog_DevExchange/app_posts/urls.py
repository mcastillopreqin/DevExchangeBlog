from django.urls import path
from . import views 
from .views import *

urlpatterns = [
   path("", views.inicio , name="inicio"),    
   path("lista", views.lista_posts, name="lista_posts"),
   path("detalle/<int:post_id>/", views.PostDetailView.as_view(), name="detalle_post"),
   path("crear_post/", views.PostCreateView.as_view(), name="crear_post"),
   path('editar/<int:pk>/', views.PostUpdateView.as_view(), name='editar_post'),
   path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='eliminar_post'),
   path("crear_etiqueta/", views.EtiquetaCreateView.as_view(), name="crear_etiqueta"),
   path("etiquetas/lista_etiquetas/", views.EtiquetaListView.as_view(), name="lista_etiquetas"),
   path("eliminar_etiqueta/<int:pk>/", views.EtiquetaDeleteView.as_view(), name="eliminar_etiqueta"),
   path('post/<int:post_id>/upvoto/', views.upvoto_post, name='upvoto_post'),
   path('post/<int:post_id>/downvoto/', views.downvoto_post, name='downvoto_post'),
   path('post/<int:post_id>/like/', views.like_post, name='like_post'),
   path('comentario/editar/<int:pk>/', views.ComentarioUpdateView.as_view(), name='editar_comentario'),
   path('eliminar_comentario/<int:pk>/', views.ComentarioDeleteView.as_view(), name='eliminar_comentario'),
     
]