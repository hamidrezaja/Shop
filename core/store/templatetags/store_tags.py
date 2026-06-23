from django import template
from store.models import ProductStatusType,ProductModel

register = template.Library()

@register.inclusion_tag("includes/latest_product.html")
def show_latest_products():
    latest_products=(ProductModel.objects.
                     filter(status=ProductStatusType.publish.value).
                     order_by('-created_date')[:8])
    return{"latest_products":latest_products}

@register.inclusion_tag("includes/related_products.html")
def related_products(slug):
    product = ProductModel.objects.get(slug=slug)
    categories = product.category.all()
    related_products = (
        ProductModel.objects
        .filter(
            status=ProductStatusType.publish.value,
            category__in=categories
        )
        .exclude(pk=product.pk)
        .distinct()
        .order_by("-created_date")[:4]
    )
    return{"related_products":related_products}