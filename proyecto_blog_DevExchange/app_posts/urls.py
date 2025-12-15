from django.urls import path
from . import views 
from .views import PostDeleteView

urlpatterns = [
   path("", views.inicio , name="inicio"),    
   path("lista", views.lista_posts, name="lista_posts"),
   path("<int:post_id>/", views.detalle_post, name="detalle_post"),
   path("crear_post/", views.PostCreateView.as_view(), name="crear_post"),
   path("crear_etiqueta/", views.EtiquetaCreateView.as_view(), name="crear_etiqueta"),
   path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='eliminar_post'),
   path('post/<int:post_id>/voto/<int:tipo>/', views.votar_post, name='votar_post'),
   path('post/<int:post_id>/upvoto/', views.upvoto_post, name='upvoto_post'),
   path('post/<int:post_id>/downvoto/', views.downvoto_post, name='downvoto_post'),
   path('post/<int:post_id>/like/', views.like_post, name='like_post'),
   path('eliminar_etiqueta/<int:etiqueta_id>/', views.eliminar_etiqueta, name='eliminar_etiqueta'),
   
]