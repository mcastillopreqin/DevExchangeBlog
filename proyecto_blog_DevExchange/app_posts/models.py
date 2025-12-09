from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count # Importamos Count para la anotación de votos

from django.contrib.auth.models import AbstractUser
from django.conf import settings

#1. Modelo de Usuario Personalizado
# Es una buena práctica usar un modelo de usuario personalizado desde el principio.
# class CustomUser(AbstractUser):
#     # Campos adicionales que quieras añadir al usuario, por ejemplo:
#     bio = models.TextField(max_length=500, blank=True)
#     ubicacion = models.CharField(max_length=30, blank=True)
#     fecha_nac = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.email


# 2. Modelo de Etiqueta (Tag)
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    #Un slug es una cadena que solo puede incluir caracteres, números, guiones y guiones bajos. Es la parte de una URL que identifica una página específica en un sitio web, de forma intuitiva.
    slug = models.SlugField(unique=True) 

    def __str__(self):
        return self.nombre

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    etiqueta = models.ManyToManyField(Etiqueta, related_name='posts')
    creado = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now, blank=True, null=True)
    imagen = models.ImageField(upload_to='media/img', blank=True, null=True)
    voto_totales = models.ManyToManyField(User, through='Voto', related_name='voted_posts', blank=True)
    
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
    
    @property
    def total_votos(self):
        # Propiedad para obtener el total de votos (positivos - negativos)
        return self.votos.filter(tipo_voto=Voto.UPVOTO).count() - self.votos.filter(tipo_voto=Voto.DOWNVOTO).count()


    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_publicacion']

# 4. Modelo de Voto
# Este modelo gestiona la relación entre un usuario, un post y el tipo de voto.
class Voto(models.Model):
    UPVOTO = 1
    DOWNVOTO = -1
    TIPO_VOTOS = (
        (UPVOTO, 'Upvote'),
        (DOWNVOTO, 'Downvote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votos')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votos')
    tipo_voto = models.SmallIntegerField(choices=TIPO_VOTOS)
    fecha_voto = models.DateTimeField(default=timezone.now)

    class Meta:
        # Asegura que un usuario solo pueda votar una vez por artículo.
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} voto {self.get_tipo_voto_display()} on {self.post.titulo}"
    
    # 5. Modelo de Comentario
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    # Permite anidación simple de comentarios si se desea,
    # referenciando al comentario padre.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_active = models.BooleanField(default=True) # Para moderar comentarios si es necesario

    class Meta:
        ordering = ['fecha_creacion'] # Muestra los comentarios más antiguos primero

    def __str__(self):
        return f"Comentado por {self.autor.username} on {self.post.titulo[:20]}"