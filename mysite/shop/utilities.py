from .models import ProductShop


def search_products_in_shop(name_of_product):
    similar_symbols = int(len(name_of_product) / 2)
    products = ProductShop.objects.all()
    similar_products = []
    for product in products:
        matches = sum([1 for a, b in zip(name_of_product, product.name) if a == b])
        if matches > similar_symbols or name_of_product.lower() == product.name.lower():
            similar_products.append(product)

    return ProductShop.objects.filter(pk__in=[product.pk for product in similar_products])


def filter_products_in_shop(queryset: ProductShop, sort_param=None):
    if sort_param is not None:
        if sort_param == 'expensive_first':
            queryset = queryset.order_by('-price')
        elif sort_param == 'first_cheap':
            queryset = queryset.order_by('price')

    return queryset.all()
