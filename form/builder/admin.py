from django.contrib import admin
from form.builder import mixins
from form.builder.models import Form, Response, Question, Answer


# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    readonly_fields = (
        'created_at',
        'updated_at'
    )
    extra = 0


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_per_page = 15
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = (
        QuestionInline,
    )
    list_display = (
        'id',
        'name',
        'slug',
        'created_at',
        'updated_at'
    )
    readonly_fields = (
        'created_at',
        'updated_at'
    )


class AnswerInline(admin.StackedInline):
    model = Answer
    readonly_fields = (
        'question',
        'text',
        'created_at',
        'updated_at'
    )
    can_delete = False
    max_num = -1
    extra = 0


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin, mixins.ExportCsvMixin):
    list_per_page = 15
    date_hierarchy = 'created_at'
    inlines = (
        AnswerInline,
    )
    search_fields = (
        'name',
    )
    actions = (
        'export_as_csv',
    )
    list_display = (
        'id',
        'name',
        'slug',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'form',
    )
    readonly_fields = (
        'form',
        'created_at',
        'updated_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
