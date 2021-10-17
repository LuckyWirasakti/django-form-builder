import csv

from crum import get_current_request
from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from form.builder.models import Form, Question


class BuilderFormMixin:
    context_name = 'builder_'

    def _get_default_fields(self):
        self.builder = get_object_or_404(
            Form,
            pk=get_current_request().GET.get('builder', None)
        )
        self.fields['form'].widget = forms.HiddenInput()
        self.fields['form'].initial = self.builder
        return self.fields

    def _get_builder_fields(self):
        builders = Question.objects.filter(form=self.builder)
        for builder in builders:
            field_name = f'{self.context_name}{builder.text}'
            if builder.choice == Question.TEXT:
                self.fields[field_name] = forms.CharField(
                    label=builder.text,
                    required=True
                )
            if builder.choice == Question.LONG_TEXT:
                self.fields[field_name] = forms.CharField(
                    required=True,
                    label=builder.text,
                    widget=forms.Textarea
                )
            if builder.choice == Question.ATTACHMENT:
                self.fields[field_name] = forms.FileField()
        return self.fields

    def _save_related_fields(self, response):
        for key, val in self.cleaned_data.items():
            if key.startswith(self.context_name):
                response.answer_set.create(
                    question=Question.objects.get(text=key.replace(
                        self.context_name, '')
                    ),
                    text=val
                )


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export selected responses"
