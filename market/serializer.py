from rest_framework import serializers
from .models import Market, MarketItem


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['town', 'city', 'district', 'region', 'type']


class MarketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketItem
        fields = ['type', 'price', 'quantity']
