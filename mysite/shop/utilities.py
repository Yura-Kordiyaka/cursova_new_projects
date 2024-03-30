from .models import ProductShop


def search_products_in_shop(name_of_product):
    products = ProductShop.objects.filter(name__icontains=name_of_product)
    return products


def filter_products_in_shop(queryset: ProductShop, sort_param=None):
    if sort_param is not None:
        if sort_param == 'expensive_first':
            queryset = queryset.order_by('price')
        elif sort_param == 'first_cheap':
            queryset = queryset.order_by('-price')

    return queryset.all()
