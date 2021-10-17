from django import forms
from form.builder import mixins
from form.builder.models import Response


class RenderForm(forms.ModelForm, mixins.BuilderFormMixin):
    class Meta:
        model = Response
        fields = (
            'form',
        )

    def __init__(self, *args, **kwargs):
        super(RenderForm, self).__init__(*args, **kwargs)
        self._get_default_fields()
        self._get_builder_fields()

    def save(self, commit=True):
        self._save_related_fields(
            super(RenderForm, self).save(commit)
        )