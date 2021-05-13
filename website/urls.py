from django.urls import path
from . import views
from api import views as apiviews

urlpatterns = [
    path('', views.home, name='website-home'),
    path('graphics/', views.graphs, name='graphics'),
    path('details/', views.details, name='query-results'),
    path('map/', views.get_map, name='tweets-map'),
    path('trends/', views.trends, name='trends')
]
