from django.core.paginator import Paginator


DEALS_ON_PAGES = 20
TRADERS_ON_PAGES = 10


def get_deals_paginator(deals, request):
    paginator = Paginator(deals, DEALS_ON_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_traders_paginator(traders, request):
    paginator = Paginator(traders, TRADERS_ON_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
