from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import pagina_404
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler404 = pagina_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app_posts.urls"), name="inicio"),
    # path("", include("app_posts.urls"),name="index"),   
    # urls de app_posts
    path("posts/", include("app_posts.urls")), 
    # urls de app_usuarios
    path("usuarios/", include("app_usuarios.urls")),
    path("contactos/", include("app_contactos.urls"), name="contacto"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)