from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarketListView, MarketDetailView, MarketCreationView, MarketCreationTemplateView,
    MarketListPage, MarketUpdateView, MarketItemUpdateView, AddMoreMarketItemView,
    MarketItemDetailView, MarketItemCreation, success_added_marketitems,
    MarketItemViewSet, MarketViewSet
)

app_name = 'market'
router = DefaultRouter()
router.register('markets', MarketViewSet)
router.register('marketitems', MarketItemViewSet)


urlpatterns = [
    path('', MarketListView.as_view(), name='market_list'),
    path('api/', include(router.urls)),
    path('list-query/', MarketListPage.as_view(), name='market_list-query'),
    path('create/', MarketCreationTemplateView.as_view(), name='market_create'),
    path('create-forms/', MarketCreationView.as_view(), name='market_create_forms'),
    path('add-market-items/<market_pk>/', AddMoreMarketItemView.as_view(), name='market_item_add'),
    path('add-item/<market_pk>/', MarketItemCreation.as_view(), name='item_add'),
    path('item-added-successfully/<marketitem_pk>/', success_added_marketitems, name='item_added-successfully'),
    path('update/<slug:slug>/<int:pk>/', MarketUpdateView.as_view(), name='market_update'),
    path('<slug:slug>/<int:pk>/', MarketDetailView.as_view(), name='market_detail'),
    path('item-update/<slug:slug>/<int:pk>/', MarketItemUpdateView.as_view(), name='market_item_update'),
    path('items-detail/<slug:slug>/<int:pk>/', MarketItemDetailView.as_view(), name='item_detail'),
]
