from django.urls import path
from . import views

urlpatterns = [
    path('list', views.PostExtraFilterView.as_view(), name='post-collection'),
]
