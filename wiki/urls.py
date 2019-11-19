from django.urls import path
from django.views.generic import TemplateView
from wiki.views import PageListView, PageCreateView,PageDetailView


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    path('page/create/', PageCreateView.as_view(), name='wiki-create-page')
]
