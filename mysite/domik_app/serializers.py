from rest_framework import serializers
from models import *

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
    category = CategorySerializer()
    class Meta:
        model = House
        fields = ['id', 'category', 'title', 'bathroom', 'bathrooms_place', 'video', 'check_in_time',
                  'departure_time', 'type_of_housing', 'address', 'floor', 'area', 'plot', 'count_people', 'weekdays_title',
                  'weekdays_price', 'saturday_title', 'saturday_price', 'friday_title', 'friday_price', 'sunday_title', 'sunday_price',
                  'pledge_title', 'pledge_price', 'weekends_title', 'weekends_price', 'new_year_title', 'new_year_price',
                  'party_title', 'party_price', 'description', 'additional_fees', 'important_information']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'