
from django.urls import path

from . import views
urlpatterns =[
    path('search/', views.search_manga, name='search_manga'),
    path('manga_list/', views.get_manga_list, name='get_manga_list'),
    path('manga_detail/', views.get_manga_detail, name='get_manga_detail'),
    path('top_manga/', views.get_top_manga, name='get_top_manga'),
    path('latest_updated/', views.get_latest_manga, name='get_latest_manga'),
]