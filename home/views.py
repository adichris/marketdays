from django.shortcuts import render
from django.views.generic import TemplateView
from market.models import Market, MarketItem


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["market_total"] = Market.objects.count()
        context["marketitem_total"] = MarketItem.objects.count()
        context["market_list"] = Market.objects.all()
        context["market_details"] = [
            ("Market Details", "Information about the market"),
            ("Market Items", "Information about the market items"),
            ("Market Population", "Information about the market population"),
            ("Market Price", "Information about the market price")
        ]
        return context
