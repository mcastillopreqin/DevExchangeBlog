from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Post, Voto, Etiqueta, Comentario

def inicio(request):
    return render(request, 'inicio.html')

def lista_posts(request):        
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    return render(request, 'lista_posts.html', {'posts': posts})

def detalle_post(request, post_id):
    comentarios = get_object_or_404(Comentario, post_id=post_id)
    post = get_object_or_404(Post, id=post_id, estado='publicado')
    return render(request, 'detalle_post.html', {'post': post, 'comentarios': comentarios})


@login_required
@require_POST  # Solo permite peticiones POST a esta vista
def voto_post(request, post_id, tipo_voto):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    # Asegúrate de que el tipo de voto sea válido (1 o -1)
    if tipo_voto not in [Voto.UPVOTO, Voto.DOWNVOTO]:
        return JsonResponse({'status': 'error', 'message': 'Invalid vote type'}, status=400)

    try:
        # Intenta obtener el voto existente del usuario para este artículo
        voto = Voto.objects.get(user=user, post=post)
        
        if voto.tipo_voto == tipo_voto:
            # Si el usuario hace clic en el mismo voto de nuevo, se asume que quiere eliminarlo (toggle)
            voto.delete()
            message = 'Voto eliminado'
        else:
            # Si cambia de opinión (de upvote a downvote o viceversa), actualiza el voto
            voto.tipo_voto = tipo_voto
            voto.save()
            message = 'Voto actualizado'

    except Voto.DoesNotExist:
        # Si no existe el voto, es creado uno nuevo
        Voto.objects.create(user=user, post=post, tipo_voto=tipo_voto)
        message = 'Voto creado'
    
    except IntegrityError:
        # Maneja cualquier otro error potencial (aunque unique_together ya lo previene)
        return JsonResponse({'status': 'error', 'message': 'No se puede procesar el voto'}, status=500)

    # Devuelve el nuevo total de votos para actualizar la UI sin recargar
    new_total_votos = post.total_votos
    return JsonResponse({
        'status': 'success',
        'message': message,
        'total_votos': new_total_votos,
        'post_id': post_id
    })
