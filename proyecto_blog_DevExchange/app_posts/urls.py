from django.urls import path
from . import views 
#from .views import PostDetailView

urlpatterns = [
   path("", views.inicio , name="inicio"),    
   path("lista", views.lista_posts, name="lista_posts"),
   path("<int:post_id>/", views.detalle_post, name="detalle_post"),
   #path("<int:pk>/", PostDetailView.as_view(), name="detalle_post"),
  # path('<int:pk>/', views.PostDetailView.as_view(), name='detalle_post'),
   #path("post/<int:post_id>/", views.detalle_post, name="detalle_post"),      
   path('<int:post_id>/handle_vote_view/<int:tipo_voto>/', views.voto_post, name='voto_post'),
]