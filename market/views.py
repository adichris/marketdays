from django.shortcuts import reverse, redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DateDetailView, UpdateView, DeleteView, TemplateView, CreateView
from .models import MarketCalendar, Market, MarketItem
from formtools.wizard.views import SessionWizardView
from .form import MarketForm, MarketCalendarForm, MarketItemForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
from rest_framework import viewsets
from .serializer import MarketSerializer, MarketItemSerializer


class MarketListView(ListView):
    model = Market
    template_name = 'market/list.html'
    context_object_name = 'market_list'


class MarketListPage(ListView):
    model = Market
    template_name = 'market/list_component.html'
    context_object_name = 'market_list'

    def get_queryset(self):
        return Market.objects.search(query=self.request.GET.get('q') or '')

    def get_context_data(self, **kwargs):
        context = super(MarketListPage, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class MarketDetailView(DetailView):
    model = Market
    slug_field = 'slug'
    pk_url_kwarg = 'pk'
    template_name = "market/market.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = str(self.object)
        ctx["market_items"] = self.object.get_market_items()
        return ctx


class MarketCreationView(SessionWizardView):
    form_list = [
        MarketForm, MarketCalendarForm, MarketItemForm
    ]
    template_name = "market/crud/create.html"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "market_photos"))

    def done(self, form_list, **kwargs):
        market_instance = form_list.pop(0).save()
        for form in form_list:
            form.instance.market = market_instance
            form.save()
        ctx = {
            "title": "New Market Created Successfully",
            "market_name": market_instance.name,
            "market_detail_url": market_instance.get_absolute_url()
        }
        return render(self.request, "market/crud/create-success.html", ctx)


class MarketUpdateView(UpdateView):
    model = Market
    form_class = MarketForm
    template_name = "market/crud/update.html"
    slug_field = 'slug'
    pk_url_kwarg = 'pk'
    slug_url_kwarg = "slug"


class MarketCreationTemplateView(TemplateView):
    template_name = "market/creation.html"

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content["title"] = "New Market"

        return content


class MarketItemCreation(CreateView):
    form_class = MarketItemForm
    template_name = "market/item/create_more.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["market_pk"] = self.kwargs["market_pk"]
        success = self.request.session.get("success", False)
        message = self.request.session.get("message")
        if success and message:
            context["message"] = message
            context["success"] = True
            context["name"] = self.request.session.get("name")
            context["modified"] = self.request.session.get("modified")
            del self.request.session["message"]
            del self.request.session["success"]
            del self.request.session["name"]
            del self.request.session["modified"]
        return context

    @property
    def market_instance(self):
        return get_object_or_404(Market, pk=self.kwargs["market_pk"])

    def get_success_url(self):
        messages.success(request=self.request, message="Successfully created market item", extra_tags="alert-success",)
        if self.request.POST.get("complete") == "done":
            return reverse("market:item_added-successfully", kwargs={"marketitem_pk": self.object.pk})
        return reverse("market:item_add", kwargs={"market_pk": self.market_instance.pk})

    def form_valid(self, form):
        form.instance.market = self.market_instance
        self.request.session["name"] = form.instance.name
        self.request.session["modified"] = form.instance.modified
        self.request.session["success"] = True
        self.request.session["message"] = "Successfully created market item"
        print(self.request.POST)
        return super().form_valid(form)


def success_added_marketitems(request, marketitem_pk):
    marketitem = get_object_or_404(MarketItem, pk=marketitem_pk)
    return render(request, "market/item/success-added-more.html", {"marketitem": marketitem})


class AddMoreMarketItemView(TemplateView):
    template_name = "market/item/add_more_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Market Items"
        context["market_pk"] = self.kwargs["market_pk"]
        context["market"] = get_object_or_404(Market, pk=self.kwargs["market_pk"])
        return context


class MarketItemUpdateView(UpdateView):
    model = MarketItem
    form_class = MarketItemForm
    template_name = "market/crud/update.html"
    slug_field = 'slug'
    slug_url_kwarg = "slug"


class MarketItemDetailView(DetailView):
    model = MarketItem
    template_name = "market/item/details.html"
    slug_field = 'slug'
    slug_url_kwarg = "slug"
    context_object_name = "market_item"


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketItemViewSet(viewsets.ModelViewSet):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer
