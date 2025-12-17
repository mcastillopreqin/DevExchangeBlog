from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

class ContactoUsuario(CreateView):
    template_name = 'contacto/contacto.html'
    form_class = ContactoForm
    # Redirige de nuevo al formulario usando el namespace correcto
    success_url = reverse_lazy('app_contactos:contacto')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tu mensaje ha sido enviado con éxito. ¡Gracias por contactarnos!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al enviar tu mensaje. Por favor, verifica los datos e inténtalo de nuevo.')
        return super().form_invalid(form)