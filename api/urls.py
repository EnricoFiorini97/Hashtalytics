from django.urls import path 
from api import views


urlpatterns = [
        path('user/<str:user>/', views.display_user, name="display_user"),
        path('hashtag/<str:hashtag>/', views.display_hashtag, name="display_hashtag"),
        path('text/<str:text>/', views.display_text, name="display_text"),
        path("trends/", views.display_trends, name="display_trends"),
        path("timeline/<str:user>/", views.display_timeline, name="display_timeline"),
        path("location/<str:lat>/<str:lon>/<str:rad>/", views.display_location, name="display_location"),
]