from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


Floor_CHOICES = [(str(i), str(i)) for i in range(1, 5)]

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar')

class Category(models.Model):
    category_name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='category_image/')

    def __str__(self):
        return self.category_name


class Domik(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField()

    def __str__(self):
        return self.title




class House(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    bathroom = models.PositiveSmallIntegerField(default=0)
    bathrooms_place = models.PositiveSmallIntegerField(default=0)
    entry = models.PositiveSmallIntegerField()
    departure = models.PositiveSmallIntegerField()
    table_tennis = models.BooleanField(default=False)
    bath_house = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    air_hockey = models.BooleanField(default=False)
    bathhouse_without_brooms = models.BooleanField(default=False)
    billiards = models.BooleanField(default=False)
    video = models.URLField()
    check_in_time = models.TimeField()
    departure_time = models.TimeField()
    type_of_housing = models.CharField(max_length=64)
    address = models.CharField(max_length=200)
    floor = models.CharField(max_length=1, choices=Floor_CHOICES, default=1)
    area = models.PositiveSmallIntegerField()
    plot = models.PositiveSmallIntegerField()
    count_people = models.PositiveSmallIntegerField(default=1)
    weekdays_title = models.CharField(max_length=24)
    weekdays_price = models.PositiveIntegerField()
    saturday_title = models.CharField(max_length=24)
    saturday_price = models.PositiveIntegerField()
    friday_title = models.CharField(max_length=24)
    friday_price = models.PositiveIntegerField()
    sunday_title = models.CharField(max_length=24)
    sunday_price = models.PositiveIntegerField()
    pledge_title = models.CharField(max_length=24)
    pledge_price = models.PositiveIntegerField()
    weekends_title = models.CharField(max_length=200)
    weekends_price = models.PositiveIntegerField()
    new_year_title = models.CharField(max_length=200)
    new_year_price = models.PositiveIntegerField()
    party_title = models.CharField(max_length=200)
    party_price = models.PositiveIntegerField()
    description = models.TextField()
    additional_fees = models.TextField()
    important_information = models.TextField()

    def clean(self):
        super().clean()
        if self.entry > self.departure:
            raise ValidationError("'entry' can't be higher than 'departure'")

    def __str__(self):
        return self.title


    def get_avg_rating(self):
        reviews = self.house_review.all()
        if reviews.exists():
            return round(sum(r.service_score for r in reviews if r.service_score) / reviews.count(), 1)
        return None

    def get_count_reviews(self):
        return self.house_review.count()

class HouseImage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_images')
    image = models.ImageField(upload_to='house_image/')

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_review')
    service_score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteHouse(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='favorite_houses')
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.house} {self.favorite}'

    class Meta:
        unique_together = ('house', 'favorite')
