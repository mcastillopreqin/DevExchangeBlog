from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import pagina_404
from app_posts.views import inicio, acerca
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler404 = pagina_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", inicio, name="inicio"),    
    path("acerca/", acerca, name="acerca"),
    path("posts/", include("app_posts.urls")),    
    path("usuarios/", include("app_usuarios.urls")),
    path("contactos/", include(("app_contactos.urls", "app_contactos"), namespace="app_contactos")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)