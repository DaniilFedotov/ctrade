from django.shortcuts import render

from .models import Deal, Trader


def deals(request):
    deals_objects = Deal.objects.all()
    context = {
        'deals': deals_objects,
    }
    return render(request, 'deals/deals.html', context)


def traders(request):
    traders_objects = Trader.objects.all()
    context = {
        'traders': traders_objects,
    }
    return render(request, 'deals/traders.html', context)
