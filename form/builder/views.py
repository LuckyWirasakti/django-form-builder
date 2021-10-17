from django.views import generic
from django.contrib.messages import views
from form.builder.forms import RenderForm


class RenderView(views.SuccessMessageMixin, generic.CreateView):
    form_class = RenderForm
    template_name = 'render.html'
    success_message = 'Response was saved successfully'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
