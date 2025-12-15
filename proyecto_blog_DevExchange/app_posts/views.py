from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError, models

from .forms import CrearPostForm, NuevaEtiquetaForm
from .models import Post, Voto, Etiqueta, Comentario
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
def inicio(request):
    return render(request, 'lista_posts.html', {'posts': Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')})

class PostCreateView(CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = "crear_post.html"
    fields = ['titulo', 'contenido', 'etiqueta', 'imagen', 'estado']
    success_url = reverse_lazy("lista_posts")

class EtiquetaCreateView(CreateView):
    model = Etiqueta
    form_class = NuevaEtiquetaForm
    template_name = "etiquetas/crear_etiqueta.html"
   
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('app_posts:crear_posts')
   

def lista_posts(request):        
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    return render(request, 'lista_posts.html', {'posts': posts})
        
def detalle_post(request, post_id):       
        post = get_object_or_404(Post, id=post_id, estado='publicado')
        comentarios = post.comments.filter(is_active=True, parent__isnull=True)
        
        # Obtener el voto actual del usuario si está autenticado
        user_vote = 0
        if request.user.is_authenticated:
            voto = post.votos.filter(usuario=request.user).first()
            if voto:
                user_vote = voto.valor
        
        # Calcular total de votos
        total_votos = post.votos.aggregate(
            total=models.Sum('valor')
        )['total'] or 0
        
        return render(request, 'detalle_post.html', {
            'post': post,
            'comentarios': comentarios,
            'user_vote': user_vote,
            'total_votos': total_votos
        }) 

class PostDeleteView(DeleteView):
    model = Post
    template_name = "app_posts/eliminar_post.html"
    success_url = reverse_lazy("listar_posts")

# 1 (Voto Positivo/Upvote)
# -1 (Voto Negativo/Downvote)
# 0 (Remover Voto)

@login_required
@require_POST
def votar_post(request, post_id, tipo):
    """
    Maneja votos AJAX para posts.
    Espera tipo = 1 (upvote), -1 (downvote) o 0 (remover voto).
    Devuelve JSON con total_votos, voto_actual, message.
    """
    post = get_object_or_404(Post, id=post_id)
    usuario = request.user
    
    try:
        # Buscar voto existente del usuario en este post
        voto_existente = Voto.objects.filter(usuario=usuario, post=post).first()
        
        if tipo == 0:
            # Remover voto
            if voto_existente:
                voto_existente.delete()
            voto_actual = 0
            message = "Voto eliminado"
        else:
            # Crear o actualizar voto (1 o -1)
            if voto_existente:
                voto_existente.valor = tipo
                voto_existente.save()
            else:
                Voto.objects.create(usuario=usuario, post=post, valor=tipo)
            voto_actual = tipo
            message = "Voto registrado"
        
        # Calcular total de votos del post (suma de valores)
        total_votos = post.votos.aggregate(
            total=models.Sum('valor')
        )['total'] or 0
        
        return JsonResponse({
            'total_votos': total_votos,
            'voto_actual': voto_actual,
            'message': message
        })
    
    except Exception as e:
        return JsonResponse({
            'message': f'Error al procesar voto: {str(e)}'
        }, status=400)

@login_required
def upvoto_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.voto_valor += 1
    post.save()
    return redirect('detalle_post', post_id=post.id)

@login_required
def downvoto_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.voto_valor -= 1
    post.save()
    return redirect('detalle_post', post_id=post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('detalle_post', post_id=post.id)


def eliminar_etiqueta(request, etiqueta_id):
    etiqueta = get_object_or_404(Etiqueta, id=etiqueta_id)
    if request.method == 'POST':
        etiqueta.delete()
        return redirect('lista_posts')
    
    return render(request, 'etiquetas/eliminar_etiqueta.html', {'etiqueta': etiqueta})