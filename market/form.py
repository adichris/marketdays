from .models import Market, MarketCalendar, MarketItem
from django import forms


class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['image', 'name', 'type', 'description', 'market_queen', 'town', 'city', 'region', 'district']
        widgets = {
            "description": forms.Textarea(attrs={'rows': 1})
        }


class MarketCalendarForm(forms.ModelForm):
    class Meta:
        model = MarketCalendar
        fields = ['date', 'month', 'notes']
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
            "notes": forms.Textarea(attrs={'rows': 1})
        }


class MarketItemForm(forms.ModelForm):
    class Meta:
        model = MarketItem
        fields = ['image', 'name', 'type', 'price', 'quantity', 'descriptions']

        widgets = {
            "descriptions": forms.Textarea(attrs={'rows': 1}),
            "image": forms.FileInput(attrs={'onchange': 'displayImage(this)'})
        }


# Market Filter
# class MarketTownSelect2(s2forms.Select2Widget):
