from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from api import views as apiviews

urlpatterns = [
    path('registration/', views.UserCreateView.as_view(), name='user-create'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='website-home'),
    path('map/', views.get_map, name='tweets-map'),
    path('trends/', views.trends, name='trends'),
    path('details/', views.details, name='query-results'),
    path('details/timeline/<str:user>', views.timeline, name='timeline'),
    path('profile/', views.profile, name='profile'),
    path('profile/set-keywords/', views.set_keywords, name='set-keywords'),
    path('profile/check-trending/<str:word>', views.check_word_trending, name='check-trending'),
    path('i18n/', include('django.conf.urls.i18n')),
]

