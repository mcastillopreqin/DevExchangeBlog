from django.shortcuts import render
from django.http import HttpResponseNotFound


def pagina_404(request, exception):
    return HttpResponseNotFound('<h1> Página no encontrada (404) </h1><p>Lo sentimos, la página que buscas no existe.</p><h1')