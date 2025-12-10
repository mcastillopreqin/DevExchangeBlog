from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Post, Voto, Etiqueta, Comentario
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
def inicio(request):
    return render(request, 'lista_posts.html', {'posts': Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')})

def lista_posts(request):        
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    return render(request, 'lista_posts.html', {'posts': posts})

# class PostsListView(ListView):
#     model = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
#     template_name = "app_posts/listar_posts.html"
#     context_object_name = "posts"
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'detalle_post.html'
#     # El nombre de la variable en el contexto será 'post' por defecto, 
#     # que es lo que espera la plantilla que te di anteriormente.

#     # Opcional: Sobrescribir el queryset para solo mostrar posts publicados
#     def get_queryset(self):
#         # Asegura que solo se puedan ver los posts que estén en estado 'publicado'
#         return Post.objects.filter(estado='publicado')
        
def detalle_post(request, post_id):
        #comentarios = get_object_or_404(Comentario, post_id=post_id)
        post = get_object_or_404(Post, id=post_id, estado='publicado')
        comentarios = post.comments.filter(is_active=True, parent__isnull=True)
        return render(request, 'detalle_post.html', {'post': post , 'comentarios': comentarios}) 


# 1 (Voto Positivo/Upvote)
# -1 (Voto Negativo/Downvote)
# 0 (Remover Voto)

@login_required
@require_POST  # Solo permite peticiones POST a esta vista
def handle_vote_view(request, post_id, tipo_voto):     
    """
    Maneja la lógica de votar un post.
    Requiere que el usuario esté autenticado y usa el método POST.
    """
    
    # 1. Obtener el Post y el usuario actual
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    # Asegúrate de que tipo_voto sea un entero
    try:
        tipo_voto = int(tipo_voto)
    except ValueError:
        return JsonResponse({'message': 'Tipo de voto inválido.'}, status=400)

    # 2. Lógica para el voto (Ejemplo simplificado)
    
    # Buscar si el usuario ya votó este post
    try:
        voto = Voto.objects.get(user=user, post=post)
    except Voto.DoesNotExist:
        voto = None

    if tipo_voto == 1 or tipo_voto == -1:
        # El usuario está votando positivamente (1) o negativamente (-1)
        
        if voto:
            if voto.value == tipo_voto:
                # Caso 1: El usuario intenta votar con el mismo valor (toggle: revierte)
                voto.delete()
                message = "Voto eliminado correctamente."
            else:
                # Caso 2: El usuario cambia el voto (de +1 a -1 o viceversa)
                voto.value = tipo_voto
                voto.save()
                message = "Voto actualizado correctamente."
        else:
            # Caso 3: El usuario vota por primera vez
            Voto.objects.create(user=user, post=post, value=tipo_voto)
            message = "Voto registrado correctamente."
            
    else:
        # Manejar cualquier otro valor de tipo_voto (ej. 0 para remover, o valores inesperados)
        if voto and tipo_voto == 0:
            voto.delete()
            message = "Voto eliminado."
        else:
            return JsonResponse({'message': 'Tipo de voto no soportado o voto inexistente para remover.'}, status=400)
    
    # 3. Recalcular el total de votos (Score)
    # Asume que tu modelo Vote tiene un campo 'value' con 1 o -1
    total_votos = Voto.objects.filter(post=post).aggregate(
        voto_valor=models.Sum('value')
    )['voto_valor'] or 0 # Si es None, lo establece en 0

    # Opcional: Actualizar el campo de score en el modelo Post
    post.score = total_votos
    post.save()
    
    # 4. Devolver la respuesta JSON
    return JsonResponse({
        'total_votos': total_votos,
        'message': message,
        'voto_actual': tipo_voto # Para actualizar la UI si es necesario
    })

# Manejo de error para usuarios no autenticados
# @login_required
# def handle_vote_view_login_required(view_func):
#     """
#     Decorador para asegurar que solo usuarios logueados puedan votar.
#     """
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             # Devuelve una respuesta 403 Forbidden para la petición AJAX
#             return JsonResponse({'message': 'Debes iniciar sesión para votar.'}, status=403)
#         return view_func(request, *args, **kwargs)
#     return wrapper


    # post = get_object_or_404(Post, id=post_id)
    # user = request.user
    
    # # Asegúrate de que el tipo de voto sea válido (1 o -1)
    # if tipo_voto not in [Voto.UPVOTO, Voto.DOWNVOTO]:
    #     return JsonResponse({'status': 'error', 'message': 'Invalid vote type'}, status=400)

    # try:
    #     # Intenta obtener el voto existente del usuario para este artículo
    #     voto = Voto.objects.get(user=user, post=post)
        
    #     if voto.tipo_voto == tipo_voto:
    #         # Si el usuario hace clic en el mismo voto de nuevo, se asume que quiere eliminarlo (toggle)
    #         voto.delete()
    #         message = 'Voto eliminado'
    #     else:
    #         # Si cambia de opinión (de upvote a downvote o viceversa), actualiza el voto
    #         voto.tipo_voto = tipo_voto
    #         voto.save()
    #         message = 'Voto actualizado'

    # except Voto.DoesNotExist:
    #     # Si no existe el voto, es creado uno nuevo
    #     Voto.objects.create(user=user, post=post, tipo_voto=tipo_voto)
    #     message = 'Voto creado'
    
    # except IntegrityError:
    #     # Maneja cualquier otro error potencial (aunque unique_together ya lo previene)
    #     return JsonResponse({'status': 'error', 'message': 'No se puede procesar el voto'}, status=500)

    # # Devuelve el nuevo total de votos para actualizar la UI sin recargar
    # new_total_votos = post.total_votos
    # return JsonResponse({
    #     'status': 'success',
    #     'message': message,
    #     'total_votos': new_total_votos,
    #     'post_id': post_id
    # })
