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
from .models import Post, Voto, Etiqueta, Comentario
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
def inicio(request):
    return render(request, 'lista_posts.html', {'posts': Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = "crear_post.html"
    success_url = reverse_lazy("lista_posts")

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
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    return render(request, 'lista_posts.html', {'posts': posts})

class PostDeleteView(DeleteView):
    model = Post
    template_name = "app_posts/eliminar_post.html"
    success_url = reverse_lazy("listar_posts")

 
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'crear_comentario.html'
    success_url = reverse_lazy('comentarios')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

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