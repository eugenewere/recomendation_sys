from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

false = False
true = True


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PropertyDetails(TimeStampMixin):
    item_id = models.IntegerField(null=False, unique=True, blank=False)
    lat = models.FloatField(default=0.000, null=true, blank=true)
    lon = models.FloatField(default=0.000, null=true, blank=true)
    country_long = models.CharField(default='', max_length=255, null=true, blank=true)
    location_name = models.CharField(default='', max_length=255, null=true, blank=true)
    route = models.CharField(default='', max_length=255, null=true, blank=true)
    sub_locality_level_1 = models.CharField(default='', max_length=255, null=true, blank=true)
    sub_locality_level_2 = models.CharField(default='', max_length=255, null=true, blank=true)
    sub_locality_level_3 = models.CharField(default='', max_length=255, null=true, blank=true)
    sub_locality_level_4 = models.CharField(default='', max_length=255, null=true, blank=true)
    sub_locality_level_5 = models.CharField(default='', max_length=255, null=true, blank=true)
    administrative_area_level_1 = models.CharField(default='', max_length=255, null=true, blank=true)
    administrative_area_level_2 = models.CharField(default='', max_length=255, null=true, blank=true)
    administrative_area_level_3 = models.CharField(default='', max_length=255, null=true, blank=true)
    administrative_area_level_4 = models.CharField(default='', max_length=255, null=true, blank=true)
    administrative_area_level_5 = models.CharField(default='', max_length=255, null=true, blank=true)
    locality = models.CharField(default='', max_length=255, null=true, blank=true)
    property_name = models.CharField(default='', max_length=255, null=true, blank=true)
    active_status = models.BooleanField(default=true)
    searchable_status = models.BooleanField(default=true)
    verification_status = models.BooleanField(default=true)
    administration_status = models.BooleanField(default=true)
    property_purpose = ArrayField(models.IntegerField(null=true, blank=true), null=True, blank=True)
    property_long_description = models.TextField(default='No Description')
    water_source = ArrayField(models.IntegerField(null=true, blank=true), null=True, blank=True)
    sewage_source = ArrayField(models.IntegerField(null=true, blank=true), null=True, blank=True)
    zoning = models.IntegerField(null=true, blank=true)
    keywords = ArrayField(models.CharField(default='', max_length=355, null=true, blank=true), null=True, blank=True)
    is_building = models.BooleanField(default=true)
    has_blocks = models.BooleanField(default=true)
    featured_status = models.BooleanField(default=true)
    views = models.PositiveIntegerField(default=0, null=true, blank=true)
    area = models.FloatField(default=0.000, null=true, blank=true)
    area_description = models.CharField(default='', max_length=255, null=true, blank=true)
    lowest_price = models.FloatField(default=0.000, null=true, blank=true)
    highest_price = models.FloatField(default=0.000, null=true, blank=true)
    single_price = models.FloatField(default=0.000, null=true, blank=true)
    negotiation = models.BooleanField(default=true)
    is_pets_allowed = models.BooleanField(default=False)
    amenities = ArrayField(models.IntegerField(null=true, blank=true), null=True, blank=True)
    rating = models.FloatField(null=true, blank=true, default=0.0)
    unit_count = models.IntegerField(null=true, blank=true, default=0)
    property_type = models.IntegerField(null=true, blank=true, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.property_name


class UsersToRecommend(TimeStampMixin):
    item_id = models.IntegerField(null=False,  unique=True,  blank=False)
    email = models.EmailField(_('email address'), unique=True, default='')
    name = models.CharField(_('name'), max_length=30, blank=True)
    session_key = models.CharField(default='', max_length=255, null=true, blank=true)

    def __str__(self):
        return '%s' % self.name


class UserInteractions(TimeStampMixin):
    user = models.ForeignKey(UsersToRecommend, on_delete=models.CASCADE, null=False)
    property = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, null=False)
    view = models.BooleanField(default=False)
    fav = models.BooleanField(default=False)
    order = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.view


class RecommendationsToUser(TimeStampMixin):
    user = models.ForeignKey(UsersToRecommend, on_delete=models.CASCADE, null=False)
    item_ids = ArrayField(models.IntegerField(null=true, blank=true), null=True, blank=True)

    def __str__(self):
        return '%s' % self.item_ids
