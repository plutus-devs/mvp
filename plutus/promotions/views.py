from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from promotions.forms import CreatePromotionForm
from promotions.models import Category, PromotionType, Promotion


@csrf_exempt
def promotion_list_apiview(request):
    

    filters = Q(status=Promotion.APPROVED)

    q = request.GET.get("q", None)
    if q != None and q != "":
        for name in q.strip().split():
            filters &= Q(name__icontains=name)

    brand = request.GET.get("brand", "-1")
    if brand and brand != "-1":
        filters &= Q(brand=brand)

    min_price = request.GET.get("min_price", "")
    min_price = request.GET.get("min_price", "")
    if min_price.replace(".", "", 1).isdigit():
        min_ = float(min_price)
        filters &= Q(min_price__gte=min_)

    max_price = request.GET.get("max_price", "")
    if max_price.replace(".", "", 1).isdigit():
        max_ = float(max_price)
        filters &= Q(max_price__lte=max_)

    flash = request.GET.get("flash", "").lower() == "true"
    # TODO: Implement flash deals

    cate_list = request.GET.getlist("cate_list", [])
    if cate_list:
        filters &= Q(category__in=cate_list)
        promotion_qs = Promotion.objects.filter(filters).all()
    else:
        promotion_qs = Promotion.objects.none()

    promotion_list = []
    for promotion in promotion_qs:
        data = {
            "pk": promotion.id,
            "name": promotion.name,
            "image": promotion.image.url
            if promotion.image
            else static("img/default_promotion.jpeg"),
            "num_member": 2,
            "left": 3,
            "url": reverse("promotions:all_deals"),
        }
        promotion_list.append(data)

    paginator = Paginator(promotion_list, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    res_data = {
        "message": {
            "promotions": page_obj.object_list,
            "hasNext": page_obj.has_next(),
        }
    }

    return JsonResponse(
        res_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


def all_deals_view(request):
    template_name = "promotions/promotion_list.html"
    context = {"title": "ALL DEALS!"}

    promotion_qs = Promotion.objects.all()

    # CAROUSEL
    carousel_qs = (
        promotion_qs.exclude(image__isnull=True)
        .exclude(image__exact="")
        .order_by("?")[:5]
    )
    carousel_list = [img.image.url for img in carousel_qs]
    context["carousel_list"] = carousel_list

    # CATEGORY LIST
    cate_id = request.GET.get("cate_id", None)
    category_qs = Category.objects.order_by("name").all()
    category_list = [
        {
            "pk": cate.id,
            "name": cate.name,
            "checked": int(cate_id) == cate.id if cate_id else True,
        }
        for cate in category_qs
    ]
    context["category_list"] = category_list

    return render(request, template_name, context)


def flash_deals_view(request):
    template_name = "promotions/promotion_list.html"
    context = {"title": "FLASH DEALS!"}

    # CATEGORY LIST
    cate_id = request.GET.get("cate_id", None)
    category_qs = Category.objects.order_by("name").all()
    category_list = [
        {
            "pk": cate.id,
            "name": cate.name,
            "checked": int(cate_id) == cate.id if cate_id else True,
        }
        for cate in category_qs
    ]
    context["category_list"] = category_list

    return render(request, template_name, context)


@login_required
def my_promotion_list_view(request):
    template_name = "promotions/my_promotion_list.html"
    context = {"title": "โปรโมชั่นที่คุณแนะนำ!"}

    filters = Q(owner=request.user)
    q = request.GET.get("q", None)
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
    if cate_list:
        filters &= Q(category__in=cate_list)
        promotion_qs = Promotion.objects.filter(filters).order_by("-created_at").all()
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
            "num_member": 2,
            "left": 3,
            "url": reverse("promotions:all_deals"),
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
    context["min_price"] = min_price
    context["max_price"] = max_price
    return render(request, template_name, context)


def category_list_view(request):
    template_name = "promotions/category_list.html"
    context = {"title": "CATEGORIES"}

    # CAROUSEL
    carousel_qs = Category.objects.order_by("?").all()
    carousel_list = [img.image.url for img in carousel_qs]
    context["carousel_list"] = carousel_list

    # CATEGORIES
    category_qs = Category.objects.order_by("name").all()
    category_list = []
    for category in category_qs:
        data = {
            "pk": category.id,
            "name": category.name,
            "image_url": category.image.url,
        }
        category_list.append(data)
    context["category_list"] = category_list

    return render(request, template_name, context)


@login_required
def create_promotion_view(request):
    template_name = "promotions/create_promotion.html"
    context = {"title": "แนะนำโปรโมชั่น"}

    if request.method == "GET":
        form = CreatePromotionForm()
        context["form"] = form
        return render(request, template_name, context)

    elif request.method == "POST":
        form = CreatePromotionForm(request.POST, request.FILES)
        if form.is_valid():

            promotion = Promotion(owner=request.user)
            for field in form.fields:
                data = form.cleaned_data.get(field)
                if field == "promotion_type":
                    promotion_type, is_created = PromotionType.objects.get_or_create(
                        name=data
                    )
                    if is_created:
                        promotion_type.save()
                    data = promotion_type

                setattr(promotion, field, data)

            promotion.save()
            messages.add_message(request, messages.SUCCESS, "ส่งคำร้องเรียบร้อยแล้ว")
            return redirect("promotions:all_deals")
        else:
            for field in form.fields:
                if field in ["description", "image"]:
                    continue
                if form[field].errors:
                    form[field].field.widget.attrs["class"] += " is-invalid"
                else:
                    form[field].field.widget.attrs["class"] += " is-valid"

            context["form"] = form
            messages.add_message(request, messages.ERROR, "ไม่สามารถโปรโมชั่นได้")
            return render(request, template_name, context)
