from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.templatetags.static import static
from django.db.models.aggregates import Min, Max, Count

from brands.models import Brand, BrandImage
from orders.models import Order
from promotions.models import Category, Promotion

def brand_list_view(request):
    template_name = "brands/brand_list.html"
    context = {"title": "BRANDS!"}

    # CAROUSEL
    carousel_qs = BrandImage.objects.order_by("?")[:4].all()
    carousel_list = [img.image.url for img in carousel_qs]
    context["carousel_list"] = carousel_list

    # BRANDS
    q = request.GET.get("q")
    filters = Q()
    if q != None and q != "":
        for name in q.strip().split():
            filters |= Q(name__icontains=name)

    brand_qs = Brand.objects.filter(filters).order_by("name").all()
    brand_list = []
    for brand in brand_qs:
        data = {
            "pk": brand.id,
            "name": brand.name,
            "cover": brand.brandimage_set.order_by("?").first().image.url,
            "is_followed": False
            if not request.user.is_authenticated
            else brand.users.filter(id=request.user.id).first() != None,
        }
        brand_list.append(data)

    context["brand_list"] = brand_list

    return render(request, template_name, context)


@login_required
def follow_brand_view(request, pk):
    brand = Brand.objects.filter(pk=pk).first()
    if brand is None:
        raise Http404

    brand.users.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def unfollow_brand_view(request, pk):
    brand = Brand.objects.filter(pk=pk).first()
    if brand is None:
        raise Http404
    brand.users.remove(request.user)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def followed_brand_list_view(request):
    template_name = "brands/brand_list.html"
    context = {"title": "BRANDS!"}

    # CAROUSEL
    carousel_qs = BrandImage.objects.order_by("?")[:4].all()
    carousel_list = [img.image.url for img in carousel_qs]
    context["carousel_list"] = carousel_list

    # BRANDS
    q = request.GET.get("q")
    filters = Q()
    if q != None and q != "":
        for name in q.strip().split():
            filters |= Q(name__icontains=name)

    brand_qs = request.user.brand_set.order_by("name").all()
    brand_list = []
    for brand in brand_qs:
        data = {
            "pk": brand.id,
            "name": brand.name,
            "cover": brand.brandimage_set.order_by("?").first().image.url,
            "is_followed": True,
        }
        brand_list.append(data)

    context["brand_list"] = brand_list

    return render(request, template_name, context)


def brand_feed_view(request, pk):
    template_name = "brands/brand_feed.html"
    context = {}

    brand = Brand.objects.filter(pk=pk).first()
    if brand is None:
        raise Http404

    context["title"] = brand.name

    # CAROUSEL
    carousel_qs = brand.brandimage_set.all()
    carousel_list = [img.image.url for img in carousel_qs]
    context["carousel_list"] = carousel_list

    filters = Q(brand=brand, status=Promotion.APPROVED)
    q = request.GET.get("q", "")
    if q != None and q != "":
        for name in q.strip().split():
            filters &= Q(name__icontains=name)

    min_price = request.GET.get("min_price", "")
    min_price = request.GET.get("min_price", "")
    if min_price.replace(".", "", 1).isdigit():
        min_ = float(min_price)
        filters &= Q(min_price__gte=min_)

    max_price = request.GET.get("max_price", "")
    if max_price.replace(".", "", 1).isdigit():
        max_ = float(max_price)
        filters &= Q(max_price__lte=max_)

    cate_list = request.GET.getlist("cate_list", None)
    if "-1" in cate_list:
        cate_list = list(map(str, Category.objects.values_list('id', flat=True)))

    if cate_list:
        filters &= Q(category__in=cate_list)
        num_member = Count("order", filter=Q(order__status__gte=Order.DEPOSIT_PAID))
        promotion_qs = Promotion.objects.filter(filters).order_by("-created_at").annotate(num_member=num_member).all()
    else:
        promotion_qs = Promotion.objects.none()

    # PROMOTION LIST
    promotion_list = []
    for promotion in promotion_qs:
        data = {
            "pk": promotion.id,
            "name": promotion.name,
            "image": promotion.image.url
            if promotion.image
            else static("img/default_promotion.jpeg"),
            "num_member": promotion.num_member,
            "left": promotion.max_member - promotion.num_member,
            "url": reverse("promotions:promotion_detail", kwargs={"pk": promotion.id}),
            "status_text": promotion.get_status_display(),
        }
        promotion_list.append(data)

    context["promotion_list"] = promotion_list

    # CATEGORY LIST
    category_qs = Category.objects.order_by("name").all()
    category_list = [
        {
            "pk": cate.id,
            "name": cate.name,
            "checked": str(cate.id) in cate_list,
        }
        for cate in category_qs
    ]
    context["category_list"] = category_list
    context["q"] = q
    context["is_followed"] = request.user in brand.users.all()
    context["brand"] = brand

    return render(request, template_name, context)

