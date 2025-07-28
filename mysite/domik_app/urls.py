from .views import *
from rest_framework import routers
from django.urls import path, include



router = routers.SimpleRouter()
# router.register(r'?', ?ViewSet, basename='?')

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('domik/', DomikListAPIView.as_view(), name='domik_list'),
    path('house/', HouseListAPIView.as_view(), name='house_list'),
    path('house/<int:pk>', HouseDetailAPIView.as_view(), name='house_detail'),
    path('favorite/add/', FavoriteCreateAPIView.as_view(), name='favorite-add'),
    path('favorite/', FavoriteListAPIView.as_view(), name='favorite-list'),
    path('favorite/<int:pk>/delete/', FavoriteDeleteAPIView.as_view(), name='favorite-delete'),
    path('reviews/add/', ReviewCreateAPIView.as_view(), name='review-add'),
    path('reviews/<int:pk>/delete/', ReviewDeleteAPIView.as_view(), name='review-delete'),
    path('reviews/house/<int:house_id>/', ReviewListAPIView.as_view(), name='review-list-by-house'),
]