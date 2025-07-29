from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        user = User(username=email, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar']

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()

    class Meta:
        model = Review
        fields = ['id', 'user', 'service_score', 'comment', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'image']


class DomikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domik
        fields = ['id', 'title', 'description']

class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'image']

class HouseListSerializer(serializers.ModelSerializer):
    house_images = HouseImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_reviews = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = House
        fields = ['id', 'category', 'title', 'bathroom', 'bathrooms_place', 'table_tennis', 'bath_house', 'swimming_pool',
                  'sauna', 'air_hockey', 'bathhouse_without_brooms', 'billiards', 'house_images', 'count_people',
                  'count_reviews', 'avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()


class HouseDetailSerializer(serializers.ModelSerializer):
    house_images = HouseImageSerializer(many=True, read_only=True)
    house_review = ReviewListSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
        model = House
        fields = ['id', 'category', 'title', 'house_images', 'bathroom', 'bathrooms_place', 'video', 'check_in_time',
                  'departure_time', 'type_of_housing', 'address', 'floor', 'area', 'plot', 'count_people',
                  'weekdays_price', 'saturday_price', 'friday_price', 'sunday_price',
                  'pledge_price', 'weekends_price', 'new_year_price',
                  'party_price', 'description', 'additional_fees', 'important_information', 'house_review',
                  ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()

class FavoriteHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHouse
        fields = ['id', 'house', 'created_date']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        favorite, _ = Favorite.objects.get_or_create(user=user)
        house = validated_data['house']
        favorite_house, _ = FavoriteHouse.objects.get_or_create(favorite=favorite, house=house)
        return favorite_house