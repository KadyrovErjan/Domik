from .serializers import *
from .models import *
from rest_framework import viewsets, generics, permissions
from .permissions import UserEdit


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DomikListAPIView(generics.ListAPIView):
    queryset = Domik.objects.all()
    serializer_class = DomikSerializer

class HouseListAPIView(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseListSerializer

class HouseDetailAPIView(generics.RetrieveAPIView):
    queryset = House.objects.all()
    serializer_class = HouseDetailSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, UserEdit]

class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        house_id = self.kwargs.get('house_id')
        return Review.objects.filter(house_id=house_id).select_related('user')

class FavoriteCreateAPIView(generics.CreateAPIView):
    serializer_class = FavoriteHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FavoriteHouse.objects.filter(favorite__user=user)

class FavoriteDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FavoriteHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FavoriteHouse.objects.filter(favorite__user=user)