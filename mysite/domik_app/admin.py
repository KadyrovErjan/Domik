from django.contrib import admin
from .models import *


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1

class HouseAdmin(admin.ModelAdmin):
    inlines = [HouseImageInline]

admin.site.register(Review)
admin.site.register(House, HouseAdmin)
admin.site.register(Domik)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(UserProfile)