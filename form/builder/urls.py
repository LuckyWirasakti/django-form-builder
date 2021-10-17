from django.urls import path
from form.builder.views import RenderView

urlpatterns = [
    path('', RenderView.as_view(), name='render'),
]