from django.shortcuts import render

from .models import Deal, Trader
from .utulities import get_deals_paginator, get_traders_paginator


def home(request):
    context = {
        'home': 'Home'
    }
    return render(request, 'deals/home.html', context)


def deals(request):
    deals_objects = Deal.objects.all()
    page_obj = get_deals_paginator(deals_objects, request)
    context = {
        'deals': deals_objects,
        'page_obj': page_obj,
    }
    return render(request, 'deals/deals.html', context)


def traders(request):
    traders_objects = Trader.objects.all()
    page_obj = get_traders_paginator(traders_objects, request)
    context = {
        'traders': traders_objects,
        'page_obj': page_obj,
    }
    return render(request, 'deals/traders.html', context)
