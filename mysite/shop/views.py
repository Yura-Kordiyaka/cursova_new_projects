from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.contrib import messages
from .models import Shop
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.models import DesiredPurchases
from django.db.models import Sum
import json
from decimal import Decimal
from .models import ProductShop
from .serializer import ProductShopSerializer
from .utilities import search_products_in_shop, filter_products_in_shop


def search_in_shop(request, name_of_product):
    search_products = search_products_in_shop(name_of_product)

    sort_by = request.GET.get("sort", None)
    search_products = filter_products_in_shop(search_products, sort_param=sort_by)
    page = request.GET.get("page", 1)
    paginator = Paginator(search_products, 10)
    try:
        search_products = paginator.page(page)
    except PageNotAnInteger:
        search_products = paginator.page(1)
    except EmptyPage:
        search_products = paginator.page(paginator.num_pages)
    search_products_data = ProductShopSerializer(search_products, many=True).data
    search_products_data = json.dumps(search_products_data)
    return render(request, 'backend/search_in_shop.html',
                  {'search_products': search_products, 'name_of_product': name_of_product, 'sort_param': sort_by,'search_products_data':search_products_data})

