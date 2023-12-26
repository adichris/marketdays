from django.contrib import admin
from .models import Market, MarketCalendar, MarketItem


admin.site.register(Market)
admin.site.register(MarketCalendar)
admin.site.register(MarketItem)