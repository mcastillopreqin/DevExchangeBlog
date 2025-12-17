from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count 
from django.conf import settings


# 1. Modelo de Etiqueta (Tag)
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    #Un slug es una cadena que solo puede incluir caracteres, números, guiones y guiones bajos. Es la parte de una URL que identifica una página específica en un sitio web, de forma intuitiva.
    slug = models.SlugField(unique=True) 

    def __str__(self):
        return self.nombre
# Modelo de Preguntas Post
class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    etiqueta = models.ManyToManyField(Etiqueta, related_name='posts')
    creado = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now, blank=True, null=True)
    imagen = models.ImageField(upload_to='media/img', blank=True, null=True)
    voto_totales = models.ManyToManyField(User, through='Voto', related_name='voted_posts', blank=True, editable=False)
    voto_valor = models.IntegerField(default=0, editable=False) # Almacena el total de votos
    ESTADO_OPCIONES = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='borrador')


    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True, editable=False)

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

# 2. Modelo de Voto
class Voto(models.Model):
    VOTO_CHOICES = (
        (1, 'Upvoto'),
        (-1, 'Downvoto'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=VOTO_CHOICES)

    class Meta:
        unique_together = ('usuario', 'post')  

# 3. Modelo de Comentario
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    voto_valor = models.IntegerField(default=0, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_active = models.BooleanField(default=True) 

    class Meta:
        ordering = ['fecha_creacion'] 

    def __str__(self):
        return f"Comentado por {self.autor.username} on {self.post.titulo[:20]}"


class ComentarioVoto(models.Model):
    VOTO_CHOICES = (
        (1, 'Upvoto'),
        (-1, 'Downvoto'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='votos')
    valor = models.IntegerField(choices=VOTO_CHOICES)

    class Meta:
        unique_together = ('usuario', 'comentario')  

    def __str__(self):
        return f"{self.usuario} -> {self.comentario_id}: {self.valor}"