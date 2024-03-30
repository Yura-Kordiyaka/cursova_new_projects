from django.utils import timezone
from .models import UserPurchases
from .models import UserShop
from datetime import datetime


def filter_user_purchase(queryset: UserPurchases, sort_param=None, date_sort=None):
    today_date = timezone.localdate()
    current_month = today_date.month
    if date_sort is not None:
        if date_sort == 'today':
            print(date_sort)
            start_of_day = datetime.combine(today_date, datetime.min.time(), tzinfo=timezone.get_current_timezone())
            end_of_day = datetime.combine(today_date, datetime.max.time(), tzinfo=timezone.get_current_timezone())
            queryset = queryset.filter(date_add__range=(start_of_day, end_of_day))
        elif date_sort == 'month':
            queryset = queryset.filter(date_add__month=current_month)

    if sort_param is not None:
        if sort_param == 'name':
            queryset = queryset.order_by('name_of_product')
        elif sort_param == 'cheap_first':
            queryset = queryset.order_by('price')
        elif sort_param == 'expensive_firs':
            queryset = queryset.order_by('-price')
        elif sort_param == 'date':
            queryset = queryset.order_by('-date_add')

    return queryset.all()


def filter_user_shops(queryset: UserShop, sort_param=None, date_sort=None):
    today_date = timezone.localdate()
    current_month = today_date.month

    if date_sort is not None:
        if date_sort == 'today':
            start_of_day = datetime.combine(today_date, datetime.min.time(), tzinfo=timezone.get_current_timezone())
            end_of_day = datetime.combine(today_date, datetime.max.time(), tzinfo=timezone.get_current_timezone())
            queryset = queryset.filter(date_add__range=(start_of_day, end_of_day))
        elif date_sort == 'month':
            queryset = queryset.filter(date_add__month=current_month)

    if sort_param is not None:
        if sort_param == 'name':
            queryset = queryset.order_by('name')
        elif sort_param == 'date':
            queryset = queryset.order_by('-date_add')

    return queryset.all()
