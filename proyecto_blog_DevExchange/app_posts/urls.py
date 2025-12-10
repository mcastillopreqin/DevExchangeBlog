from django.urls import path
from . import views 
from .views import handle_vote_view

urlpatterns = [
   path("", views.inicio , name="inicio"),    
   path("lista", views.lista_posts, name="lista_posts"),
   path("<int:post_id>/", views.detalle_post, name="detalle_post"),
   #path("<int:pk>/", PostDetailView.as_view(), name="detalle_post"),
  # path('<int:pk>/', views.PostDetailView.as_view(), name='detalle_post'),
   #path("post/<int:post_id>/", views.detalle_post, name="detalle_post"),      
   path('<int:post_id>/voto/<int:tipo_voto>/', views.handle_vote_view, name ='handle_vote'),#views.voto_post, name='voto_post'),
]