from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.messages import views
from form.builder.forms import RenderForm
from form.builder.models import Form


class RenderView(views.SuccessMessageMixin, generic.CreateView):
    form_class = RenderForm
    template_name = 'render.html'
    success_message = 'Response was saved successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(
            Form,
            slug=self.request.GET.get('builder', None)
        )
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
