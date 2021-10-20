import csv

from crum import get_current_request
from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from form.builder.models import Form, Question


class BuilderFormMixin(forms.ModelForm):
    context_name = 'builder_'

    def _builder_fields(self):
        form = get_object_or_404(
            Form,
            slug=get_current_request().GET.get('builder', None)
        )
        self.fields['form'].widget = forms.HiddenInput()
        self.fields['form'].initial = form
        builders = Question.objects.filter(form=form)
        for builder in builders:
            field_name = f'{self.context_name}{builder.text}'
            if builder.choice == Question.TEXT:
                self.fields[field_name] = forms.CharField(
                    label=builder.text,
                    required=True
                )
            if builder.choice == Question.LONG_TEXT:
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea,
                    label=builder.text,
                    required=True,
                )
            if builder.choice == Question.ATTACHMENT:
                self.fields[field_name] = forms.FileField(
                    label=builder.text,
                    required=True
                )

    def _save_related_fields(self, response):
        for key, val in self.cleaned_data.items():
            if key.startswith(self.context_name):
                if isinstance(val, InMemoryUploadedFile):
                    default_storage.save(
                        val.name, content=ContentFile(val.read()))
                response.answer_set.create(
                    question=Question.objects.get(text=key.replace(
                        self.context_name, '')
                    ),
                    text=val
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._builder_fields()

    def save(self, commit=True):
        self._save_related_fields(
            super().save(commit)
        )


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export selected responses"
