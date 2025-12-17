from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CrearPostForm, ComentarioForm, NuevaEtiquetaForm
from .models import Post,  Etiqueta, Comentario
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
def inicio(request):
    # Página de inicio: mostramos posts recientes y una galería de imágenes relacionadas
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    gallery = Post.objects.filter(estado='publicado').exclude(imagen='').exclude(imagen__isnull=True).order_by('-fecha_publicacion')[:8]
    return render(request, 'index.html', {'posts': posts, 'gallery': gallery})

class PostPorEtiquetaListView(ListView):
    model = Post
    template_name = "post_por_etiqueta.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(etiqueta=self.kwargs['pk'], estado='publicado').order_by('-fecha_publicacion')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = "crear_post.html"
    success_url = reverse_lazy("lista_posts")

class PostListView(ListView):
    model = Post
    template_name = "lista_posts.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha_publicacion')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha_publicacion')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        elif orden == 'votos':
            queryset = queryset.order_by('-voto_totales')
        elif orden == 'likes':
            queryset = queryset.order_by('-total_likes')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context
class PostDetailView(DetailView):
    model = Post
    template_name = "detalle_post.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comentario'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(post_id=self.kwargs['post_id'], is_active=True, parent__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.post = self.object
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent_id = parent_id        
            comentario.save()
            return redirect('detalle_post', post_id=self.object.id)
        
        context = self.get_context_data(form_comentario=form)
        return self.render_to_response(context)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = "editar_post.html"
    success_url = reverse_lazy("lista_posts")

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "eliminar_post.html"
    success_url = reverse_lazy("lista_posts")

class EtiquetaCreateView(LoginRequiredMixin, CreateView):
    model = Etiqueta
    form_class = NuevaEtiquetaForm
    template_name = "etiquetas/crear_etiqueta.html"
    success_url = reverse_lazy("lista_etiquetas")

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('crear_post')
   
class EtiquetaListView(ListView):
    model = Etiqueta
    template_name = "etiquetas/lista_etiquetas.html"
    context_object_name = "etiquetas"

class EtiquetaDeleteView(LoginRequiredMixin, DeleteView):
    model = Etiqueta
    template_name = "etiquetas/eliminar_etiqueta.html"
    success_url = reverse_lazy("lista_etiquetas")

def lista_posts(request):        
    posts_qs = Post.objects

    orden = request.GET.get('orden')
    if orden == 'reciente':
        posts_qs = posts_qs.order_by('-fecha_publicacion')
    elif orden == 'antiguo':
        posts_qs = posts_qs.order_by('fecha_publicacion')
    elif orden == 'alfabetico':
        posts_qs = posts_qs.order_by('titulo')
    elif orden == 'likes':
        posts_qs = posts_qs.annotate(likes_count=Count('likes')).order_by('-likes_count')
    elif orden == 'votos':
        posts_qs = posts_qs.order_by('-voto_totales')
    else:
        posts_qs = posts_qs.order_by('-fecha_publicacion')

    paginator = Paginator(posts_qs, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    borrador_count = Post.objects.filter(estado='borrador').count()

    return render(request, 'lista_posts.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'borrador_count': borrador_count,
    })

 
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'crear_comentario.html'
    success_url = reverse_lazy('comentarios')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)
    
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'
    
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('detalle_post', kwargs={'post_id': self.object.post.id})
        
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/eliminar_comentario.html'

    def get_success_url(self):
        return reverse_lazy('detalle_post', kwargs={'post_id': self.object.post.id})

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

def acerca(request):
    return render(request, 'acerca.html')