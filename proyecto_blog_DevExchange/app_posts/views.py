from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError

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
            return reverse_lazy('crear_post')
   

def lista_posts(request):        
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    return render(request, 'lista_posts.html', {'posts': posts})
        
def detalle_post(request, post_id):       
        post = get_object_or_404(Post, id=post_id, estado='publicado')
        comentarios = post.comments.filter(is_active=True, parent__isnull=True)
        return render(request, 'detalle_post.html', {'post': post , 'comentarios': comentarios}) 

class PostDeleteView(DeleteView):
    model = Post
    template_name = "app_posts/eliminar_post.html"
    success_url = reverse_lazy("listar_posts")

# 1 (Voto Positivo/Upvote)
# -1 (Voto Negativo/Downvote)
# 0 (Remover Voto)

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