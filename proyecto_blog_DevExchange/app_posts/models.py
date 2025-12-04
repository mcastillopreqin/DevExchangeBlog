from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count # Importamos Count para la anotación de votos

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    ESTADO_OPCIONES = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='borrador')

    # Campo ManyToManyField para almacenar los usuarios que han dado "like"
    # related_name='blog_posts' permite acceder a los posts a los que un usuario ha dado like desde el objeto User.
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    # Propiedad para contar fácilmente el número de likes
    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-fecha_publicacion']