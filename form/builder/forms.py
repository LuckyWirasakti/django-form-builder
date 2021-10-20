from form.builder import mixins
from form.builder.models import Response


class RenderForm(mixins.BuilderFormMixin):
    class Meta:
        model = Response
        fields = (
            'form',
        )