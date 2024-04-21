from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from .models import UserCategory, UserPurchases
from django.contrib import messages
from shop.models import Shop
from urllib.parse import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import DesiredPurchases
from django.db.models import Sum
from .utilities import filter_user_purchase, filter_user_shops
from .serializers import UserPurchaseSerializer
from .serializers import UserShopSerializer
import json
from .models import UserShop
from decimal import Decimal
from django.contrib.auth.decorators import login_required

def main(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_user')
    # else:
        return render(request, 'backend/index.html')

@login_required(login_url='login_user')
def all_category(request):
    categories = UserCategory.objects.filter(user=request.user).all()
    sort_by = request.GET.get("sort", None)
    if sort_by == 'name':
        categories = UserCategory.objects.order_by('name')
    elif sort_by == 'date':
        categories = UserCategory.objects.order_by('-date_add')
    paginator = Paginator(categories, 1)
    page = request.GET.get("page", 1)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    return render(request, 'backend/all_categories.html',
                  {'categories': categories, 'sort_param': sort_by})

@login_required(login_url='login_user')
def get_product_by_category(request, pk):
    category = UserCategory.objects.get(id=pk)
    sort_by = request.GET.get("sort", None)
    date_sort = request.GET.get('date_filter', None)
    shops = Shop.objects.all()
    user_purchases = UserPurchases.objects.filter(category=category, user=request.user).all()
    user_purchases = filter_user_purchase(queryset=user_purchases, sort_param=sort_by, date_sort=date_sort)
    all_price = user_purchases.aggregate(Sum('price'))['price__sum']
    if all_price is None:
        all_price = 0
    paginator = Paginator(user_purchases, 10)
    page = request.GET.get("page", 1)
    try:
        user_purchases = paginator.page(page)
    except PageNotAnInteger:
        user_purchases = paginator.page(1)
    except EmptyPage:
        user_purchases = paginator.page(paginator.num_pages)
    user_purchases_data = UserPurchaseSerializer(user_purchases, many=True).data
    user_purchases_json = json.dumps(user_purchases_data)
    return render(request, 'backend/category_with_purchases.html',
                  {"category": category, 'user_purchases': user_purchases, 'shops': shops, 'sort_param': sort_by,
                   'date_sort': date_sort, 'all_price': all_price, "user_purchases_data": user_purchases_json})

@login_required(login_url='login_user')
def delete_purchase(request, pk):
    user_purchase = UserPurchases.objects.get(id=pk)
    category_id = user_purchase.category.id
    messages.success(request, f'покупка {user_purchase.name_of_product} видалена успішно')
    user_purchase.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login_user')
def delete_category(request, pk):
    category = UserCategory.objects.get(id=pk)
    previous_pass = request.META.get('HTTP_REFERER')
    messages.success(request, f'Категорія {category.name} видалена успішно')
    category.delete()
    return redirect(previous_pass)

@login_required(login_url='login_user')
def specific_purchase(request, pk):
    user_purchase = UserPurchases.objects.get(id=pk)
    shops = UserShop.objects.order_by('name').all()
    categories = UserCategory.objects.order_by('name').all()
    return render(request, 'backend/specific_purchase.html', {'user_purchase': user_purchase, 'shops': shops, 'categories': categories})

@login_required(login_url='login_user')
def add_purchase(request):
    if request.method == "POST":
        if 'add_desired_purchase' in request.POST:
            name = request.POST['name_of_product']
            desired=DesiredPurchases.objects.create(name_of_product=name, user=request.user)
            messages.success(request, f"Бажана покупка {desired.name_of_product} додано успішно")
            return redirect('desired_purchase')
        else:
            user_category = UserCategory.objects.get(id=request.POST['category_id'], user=request.user)
            name_of_product = request.POST['name_of_product']
            price_of_product = request.POST['price_of_product']
            description = request.POST['description']
            shop = UserShop.objects.get(id=request.POST['shop'])
            user=UserPurchases.objects.create(user=request.user, category=user_category,
                                         price=price_of_product,
                                         name_of_product=name_of_product,
                                         shop=shop,
                                         description=description)
            messages.success(request, f'Покупка {name_of_product} успішно додана')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        shops = UserShop.objects.filter(user=request.user).all()
        categories = UserCategory.objects.filter(user=request.user).all()
        return render(request, 'backend/add_purchase.html', {'shops': shops, 'categories': categories})

@login_required(login_url='login_user')
def add_category(request):
    if request.method == "POST":
        name = request.POST['category_name']
        UserCategory.objects.create(name=name, user=request.user)
        messages.success(request, f'Категорія {name} додано успішно')
        return redirect('all_category')

@login_required(login_url='login_user')
def edit_category(request, pk):
    if request.method == "POST":
        category = UserCategory.objects.get(id=pk)
        category.name = request.POST['name']
        category.save()
        return redirect('all_category')

@login_required(login_url='login_user')
def edit_purchase(request, pk):
    if request.method == 'POST':
        price_str = request.POST['price'].replace(',', '.')
        purchase = UserPurchases.objects.get(id=pk)
        shop = UserShop.objects.get(id=request.POST['shop'])
        purchase.name_of_product = request.POST['name_of_product']
        category=request.POST['category']
        category = UserCategory.objects.get(id=category)
        purchase.category = category
        purchase.shop = shop
        purchase.description = request.POST['description']
        purchase.price = Decimal(price_str)
        purchase.save()
        return redirect(reverse('specific_purchase', args=(purchase.id,)))

@login_required(login_url='login_user')
def user_costs(request):
    sort_by = request.GET.get("sort", None)
    shops = Shop.objects.all()
    date_sort = request.GET.get('date_filter', None)
    user_purchases = UserPurchases.objects.filter(user=request.user).all()
    user_purchases = filter_user_purchase(queryset=user_purchases, sort_param=sort_by, date_sort=date_sort)
    all_price = user_purchases.aggregate(Sum('price'))['price__sum']
    if all_price is None:
        all_price = 0
    paginator = Paginator(user_purchases, 1)
    page = request.GET.get("page", 1)
    try:
        user_purchases = paginator.page(page)
    except PageNotAnInteger:
        user_purchases = paginator.page(1)
    except EmptyPage:
        user_purchases = paginator.page(paginator.num_pages)
    user_purchases_data = UserPurchaseSerializer(user_purchases, many=True).data
    user_purchases_json = json.dumps(user_purchases_data)
    return render(request, 'backend/user_costs.html',
                  {'user_purchases': user_purchases, 'all_price': all_price, 'date_sort': date_sort, 'shops': shops,
                   'user_purchases_data': user_purchases_json, 'sort_param': sort_by})

@login_required(login_url='login_user')
def desired_purchase(request):
    desired_purchase = DesiredPurchases.objects.filter(user=request.user)
    sort_by = request.GET.get("sort", None)
    if sort_by == 'name':
        desired_purchase = DesiredPurchases.objects.order_by('name_of_product')
    else:
        desired_purchase = DesiredPurchases.objects.order_by('-date_add')
    paginator = Paginator(desired_purchase, 10)
    page = request.GET.get("page", 1)
    try:
        desired_purchase = paginator.page(page)
    except PageNotAnInteger:
        desired_purchase = paginator.page(1)
    except EmptyPage:
        desired_purchase = paginator.page(paginator.num_pages)
    return render(request, 'backend/desired_purchase.html',
                  {'desired_purchase': desired_purchase, 'sort_param': sort_by})

@login_required(login_url='login_user')
def add_user_shop(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print("-------------")
            print(request.POST['address_shop'])
            address = request.POST['address_shop']
            name = request.POST['name_shop']
            shop=UserShop.objects.create(name=name, address=address, user=request.user)
            messages.success(request, f"Магазин {shop.name} додано успішно")
            return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login_user')
def user_shops(request):
    shops_query_set = UserShop.objects.filter(user=request.user)
    sort_by = request.GET.get("sort", None)
    date_sort = request.GET.get('date_filter', None)
    shops_query_set = filter_user_shops(queryset=shops_query_set, sort_param=sort_by, date_sort=date_sort)
    paginator = Paginator(shops_query_set, 1)
    page = request.GET.get("page", 1)
    try:
        shops_query_set = paginator.page(page)
    except PageNotAnInteger:
        shops_query_set = paginator.page(1)
    except EmptyPage:
        shops_query_set = paginator.page(paginator.num_pages)
    shops_query_set_data=UserShopSerializer(shops_query_set, many=True).data
    shops_query_set_json=json.dumps(shops_query_set_data)

    return render(request, 'backend/user_shop.html',
                  {'user_shops': shops_query_set, 'sort_param': sort_by, 'date_sort': date_sort,'shop_query_set_data':shops_query_set_json})

@login_required(login_url='login_user')
def delete_user_shop(request, pk):
    user_shop = UserShop.objects.get(id=pk)
    user_shop_name=user_shop.name
    messages.success(request, f'Магазин {user_shop_name} видалено успішно')
    user_shop.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login_user')
def delete_desired_purchase(request, pk):
    user_purchase = DesiredPurchases.objects.get(id=pk)
    messages.success(request, f'Бажана покупка {user_purchase.name_of_product} видалено успішно')
    user_purchase.delete()
    return redirect(request.META.get('HTTP_REFERER'))
