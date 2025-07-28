from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Domik)
class DomikTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(House)
class CountryTranslationOptions(TranslationOptions):
    fields = ('title', 'type_of_housing', 'address', 'weekdays_title', 'saturday_title', 'friday_title', 'sunday_title', 'pledge_title', 'weekends_title', 'new_year_title', 'party_title', 'description', 'additional_fees', 'important_information')