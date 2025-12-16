from django.shortcuts import render, redirect       
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import Group, User
from app_posts.models import Comentario, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy


from .forms import RegistroUsuarioForm

class UsuarioListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "app_usuarios/lista_usuarios.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "app_usuarios/eliminar_usuario.html"
    success_url = reverse_lazy("lista_usuarios")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context
    
    def post (self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios' , False)
        eliminar_posts = request.POST.get('eliminar_posts' , False)
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(autor=self.object).delete()
        if eliminar_posts:
            Post.objects.filter(autor=self.object).delete()   

        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        if es_colaborador:
            messages.error(request, 'No se puede eliminar un usuario con rol de Colaborador.')
            return redirect('lista_usuarios')
        
        messages.success(request, f'Usuario {self.object.username} eliminado exitosamente.')
        return self.delete(request, *args, **kwargs)

# registro VBF vista basada en funcion
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. Ahora puedes iniciar sesión.')
            group = Group.objects.get(name='Registrado')
            user.groups.add(group)
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores abajo.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'app_usuarios/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Has iniciado sesión como {username}.')
                return redirect('lista_posts')
            else:
                messages.error(request, 'Usuario o contraseña inválidos.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'app_usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')