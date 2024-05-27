from django.urls import path

from . import views

urlpatterns = [
    # path ('userprofile/', views.UserProfileView.as_view(), name='userprofile'),
    # path("FavManga/", views.FavMangaViewSet.as_view({'post': 'create','get': 'list','delete': 'destroy'}), name="favmanga"),
    path('add_fav_manga/', views.add_fav_manga.as_view(), name='add_fav_manga'),
    path('get_fav_manga/', views.get_fav_manga.as_view(), name='get_fav_manga'),
    path('delete_fav_manga/', views.delete_fav_manga.as_view(), name='delete_fav_manga'),
]
