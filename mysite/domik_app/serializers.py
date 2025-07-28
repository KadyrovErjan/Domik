from rest_framework import serializers
from .models import *

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
    category = CategorySerializer()
    class Meta:
        model = House
        fields = ['id', 'category', 'title', 'bathroom', 'bathrooms_place', 'table_tennis', 'bath_house', 'swimming_pool',
                  'sauna', 'air_hockey', 'bathhouse_without_brooms', 'billiards', 'house_images', 'count_people', 'weekdays_title',]



class HouseDetailSerializer(serializers.ModelSerializer):
    house_images = HouseImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_reviews = serializers.SerializerMethodField()
    house_review = ReviewListSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
        model = House
        fields = ['id', 'category', 'title', 'house_images', 'bathroom', 'bathrooms_place', 'video', 'check_in_time',
                  'departure_time', 'type_of_housing', 'address', 'floor', 'area', 'plot', 'count_people', 'weekdays_title',
                  'weekdays_price', 'saturday_title', 'saturday_price', 'friday_title', 'friday_price', 'sunday_title', 'sunday_price',
                  'pledge_title', 'pledge_price', 'weekends_title', 'weekends_price', 'new_year_title', 'new_year_price',
                  'party_title', 'party_price', 'description', 'additional_fees', 'important_information', 'house_review',
                  'count_reviews', 'avg_rating']

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