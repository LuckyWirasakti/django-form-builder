from django.contrib.messages import views
from django.shortcuts import get_object_or_404
from django.views import generic
from form.builder.forms import RenderForm
from form.builder.models import Form


class RenderView(views.SuccessMessageMixin, generic.CreateView):
    model = Form
    form_class = RenderForm
    template_name = 'render.html'
    success_message = 'Response was saved successfully'
    lookup_queryparam = 'builder'
    context_object_name = 'object'

    def get_object(self):
        return get_object_or_404(
            self.model,
            slug=self.request.GET.get(self.lookup_queryparam, None)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
