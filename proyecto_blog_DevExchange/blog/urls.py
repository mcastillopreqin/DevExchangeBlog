from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import index, pagina_404

handler404 = pagina_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app_posts.urls")), 
    # urls de app_posts
    path("posts/", include("app_posts.urls")), 
    # urls de app_usuarios
    path("usuarios/", include("app_usuarios.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
