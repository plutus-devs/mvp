from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from brands.models import Brand, BrandImage


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
    pass
