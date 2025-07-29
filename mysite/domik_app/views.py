from .serializers import *
from .models import *
from .permissions import UserEdit
from .filters import HouseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg


class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DomikListAPIView(generics.ListAPIView):
    queryset = Domik.objects.all()
    serializer_class = DomikSerializer

class HouseListAPIView(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HouseFilter
    search_fields = ['title']
    ordering_fields = ['area', 'price', 'entry', 'departure', 'floor', 'plot', 'count_people', 'weekdays_price']

class PopularHouseListAPIView(generics.ListAPIView):
    serializer_class = HouseListSerializer

    def get_queryset(self):
        return House.objects.annotate(
            avg_rating=Avg('house_review__service_score')
        ).filter(avg_rating__gte=4.0).order_by('-avg_rating')

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