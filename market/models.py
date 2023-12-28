from typing import Any
from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
import os
from djmoney.money import Money


def upload_location(instance, filename):
    return os.path.join("media", instance._meta.app_label, instance.name, filename)


class MarketManager(models.Manager):
    def search(self, query):
        return self.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query) | models.Q(type__icontains=query))
   
    def search_filter(self, city, town, district, region):
        if district and region:
            return self.filter(
                    models.Q(city__icontains=city or '') & 
                    models.Q(town__icontains=town or '') & 
                    models.Q(district__icontains=district) & 
                    models.Q(region__icontains=region)
                    )
        return self.filter(
            models.Q(city__icontains=city or '') & 
            models.Q(town__icontains=town or ''))

class Market(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120, null=True, blank=True)
    town = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    region = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True, default="Ghana")
    district = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to=upload_location)
    market_queen = models.CharField(max_length=120, null=True, blank=True, help_text="Market Queen's name")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = MarketManager()

    def get_absolute_update_url(self):
        return reverse('market:market_update', kwargs={'slug': self.slug, "pk": self.pk})

    def get_absolute_add_items_url(self):
        return reverse('market:market_item_add', kwargs={'market_pk': self.pk})

    def __str__(self):
        return f"{self.town or self.city} {self.name}"

    def get_market_items(self):
        return self.MARKET_ITEMS.all()

    def save(self, *args, **kwargs):
        self.slug = slugify((f"{self.city or ''} {self.town or ''} {self.name}"))
        return super(Market, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('market:market_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class MarketItem(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='MARKET_ITEMS')
    name = models.CharField(max_length=120, null=True, help_text="The name of the market product")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='GHS', null=True, validators=[MinValueValidator(Money(1, "GHS"))], help_text="Unit price")
    quantity = models.IntegerField(default=0, null=True, help_text="The number of this products in the market")
    slug = models.SlugField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, help_text="The image of the market product")
    descriptions = models.TextField(null=True)
    modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=60, null=True, blank=True, help_text="Market item type")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('market', 'name')
        verbose_name_plural = 'Market Items'
        verbose_name = 'Market Item'
        ordering = ['market', 'name', 'quantity']

    def get_absolute_url(self):
        return reverse('market:item_detail', kwargs={'slug': self.slug, "pk": self.pk})

    def get_absolute_update_url(self):
        return reverse('market:market_item_update', kwargs={'slug': self.slug, "pk": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.market.name} {self.name}")
        return super().save(*args, **kwargs)


class MonthChoice(models.IntegerChoices):
    JANUARY = 1, "January"
    FEBRUARY = 2, "February"
    MARCH = 3, "March"
    APRIL = 4, "April"
    MAY = 5, "May"
    JUNE = 6, "June"
    JULY = 7, "July"
    AUGUST = 8, "August"
    SEPTEMBER = 9, "September"
    OCTOBER = 10, "October"
    NOVEMBER = 11, "November"
    DECEMBER = 12, "December"


class MarketCalendar(models.Model):
    date = models.DateField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True, choices=MonthChoice.choices)
    notes = models.TextField(null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Market Calendar'
        verbose_name_plural = "Market Calendars"

    def save(self, *args, **kwargs):
        return str(self.date)
