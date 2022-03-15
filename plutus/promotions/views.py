from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Min, Max, Count, Sum

from promotions.forms import CreatePromotionForm
from promotions.models import Category, PromotionType, Promotion
from orders.models import Order


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

    cate_list = request.GET.getlist("cate_list", [])
    if cate_list:
        filters &= Q(category__in=cate_list)
        num_member = Count("order", filter=Q(order__status__gte=Order.DEPOSIT_PAID))
        total_price = Sum(
            "order__full_price", filter=Q(order__status__gte=Order.DEPOSIT_PAID)
        )
        promotion_qs = (
            Promotion.objects.filter(filters)
            .order_by("-created_at")
            .annotate(
                num_member=num_member,
                total_price=total_price,
            )
            .all()
        )
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
            "num_member": promotion.num_member,
            "url": reverse("promotions:promotion_detail", kwargs={"pk": promotion.id}),
            "status_text": promotion.get_status_display(),
        }

        left = 100
        if promotion.type == Promotion.BY_NUMBER and promotion.max_member:
            left = promotion.max_member - promotion.num_member
            data["left"] = f"ขาดอีก {left:,} รายการ"

        elif promotion.type == Promotion.BY_PRICE and promotion.threshold:
            left = promotion.total_price if promotion.total_price else 0.0
            data["left"] = f"ต้องการอีก {promotion.threshold - left:,} ฿"

        if not flash:
            promotion_list.append(data)

        elif promotion.type == Promotion.BY_NUMBER and left <= 1:
            promotion_list.append(data)

        elif promotion.type == Promotion.BY_PRICE and left <= 500.00:
            promotion_list.append(data)

    paginator = Paginator(promotion_list, 12)
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
    context = {"title": "โพสต์ที่คุณสร้าง!"}

    filters = Q(owner=request.user)
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
        cate_list = list(map(str, Category.objects.values_list("id", flat=True)))

    if cate_list:
        filters &= Q(category__in=cate_list)
        num_member = Count("order", filter=Q(order__status__gte=Order.DEPOSIT_PAID))
        total_price = Sum(
            "order__full_price", filter=Q(order__status__gte=Order.DEPOSIT_PAID)
        )
        promotion_qs = (
            Promotion.objects.filter(filters)
            .order_by("-created_at")
            .annotate(
                num_member=num_member,
                total_price=total_price,
            )
            .all()
        )
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
            "url": reverse("promotions:promotion_detail", kwargs={"pk": promotion.id}),
            "status_text": promotion.get_status_display(),
        }
        if promotion.type == Promotion.BY_NUMBER and promotion.max_member:
            left = promotion.max_member - promotion.num_member
            data["left"] = f"ขาดอีก {left:,} รายการ"

        elif promotion.type == Promotion.BY_PRICE and promotion.threshold:
            left = promotion.total_price if promotion.total_price else 0.0
            data["left"] = f"ต้องการอีก {promotion.threshold - left:,} ฿"

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
    context["q"] = q
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
            "url": reverse("promotions:all_deals") + f"?cate_id={category.id}",
        }
        category_list.append(data)
    context["category_list"] = category_list

    return render(request, template_name, context)


@login_required
def create_promotion_view(request):
    template_name = "promotions/create_promotion.html"
    context = {"title": "สร้างโพสต์"}

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


def promotion_detail_view(request, pk):
    template_name = "promotions/promotion_detail.html"
    context = {}

    num_member = Count("order", filter=Q(order__status__gte=Order.DEPOSIT_PAID))
    total_price = Sum(
        "order__full_price", filter=Q(order__status__gte=Order.DEPOSIT_PAID)
    )
    promotion = (
        Promotion.objects.filter(id=pk)
        .annotate(num_member=num_member, total_price=total_price)
        .first()
    )
    if not promotion:
        raise Http404

    is_approved = promotion.status == Promotion.APPROVED
    is_owner = request.user.is_authenticated and promotion.owner == request.user
    has_access = (is_approved) or (is_owner)
    if not has_access:
        raise PermissionDenied

    data = {
        "pk": promotion.id,
        "name": promotion.name,
        "close_date": promotion.close_at.strftime("%d/%m/%Y"),
        "url": promotion.url,
        "description": promotion.description,
        "image": promotion.image.url if promotion.image else None,
        "status_text": promotion.get_status_display(),
        "show_status": is_owner,
        "is_approved": is_approved,
    }

    if promotion.type == Promotion.BY_NUMBER:
        data["max_member"] = promotion.max_member
        data["num_member"] = promotion.num_member

    elif promotion.type == Promotion.BY_PRICE:
        data["max_member"] = promotion.threshold
        data["num_member"] = promotion.total_price if promotion.total_price else 0.0

    context["title"] = promotion.name
    context["promotion"] = data

    if request.user.is_authenticated:
        order_qs = Order.objects.filter(promotion=promotion).order_by("status0").all()
        order_list = []
        all_order_list = []
        total = 0
        discount_price = 0
        our_total = 0
        for order in order_qs:
            data = {
                "pk": order.id,
                "product_id": order.product_id,
                "product_name": order.product_name,
                "discount_price": f"{order.discount_price:,}",
                "status": order.status,
                "status_text": order.get_status_display(),
            }
            if order.status >= Order.APPROVED:
                total += order.full_price
                all_order_list.append(data)

            if order.user == request.user:
                order_list.append(data)
                if order.status >= Order.APPROVED:
                    our_total += order.full_price
                    discount_price += order.discount_price


        context["order_list"] = order_list
        context["total_price"] = f"{total:,}"
        context["discounted_price"] = f"{our_total - discount_price:,}"
        context["all_order_list"] = all_order_list

    return render(request, template_name, context)
