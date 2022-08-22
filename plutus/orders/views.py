from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from orders.models import Order
from orders.forms import UploadDeposit, UploadImageForm
from promotions.models import Promotion


@login_required
def create_order_view(request, promotion_pk):
    res = str(request.POST.dict())

    promotion = Promotion.objects.filter(id=promotion_pk).first()
    if not promotion:
        raise Http404

    if request.method == "POST":
        order_dict = {}
        for key, value in request.POST.dict().items():
            if key == "csrfmiddlewaretoken":
                continue

            field, _id = key.split("_")

            if _id not in order_dict.keys():
                order_dict[_id] = {field: value}
            else:
                order_dict[_id][field] = value

        for _, data in order_dict.items():
            order = Order(
                promotion=promotion,
                user=request.user,
                product_id=data["productcode"],
                full_price=data["productprice"],
                description=data["productdescription"],
            )
            order.save()

        messages.add_message(request, messages.SUCCESS, "ส่งคำร้องเรียบร้อยแล้ว")
        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def order_detail_view(request, pk):
    template_name = "orders/order_detail.html"
    context = {}

    order = Order.objects.filter(pk=pk, user=request.user).first()
    if order == None:
        raise Http404

    context["order"] = {
        "pk": order.id,

        "image": order.promotion.image.url,
        "promotion_name": order.promotion.name,

        "product_name": order.product_name,
        "product_id": order.product_id,
        "status_text": order.get_status_display(),
        "description": order.description,

        "can_see_promotion": order.promotion.status == Promotion.APPROVED,
        "promotion_url": reverse("promotions:promotion_detail", kwargs={"pk": order.promotion.id}),

        "deposit": f"{order.deposit:,}",
        "dept": f"{order.dept:,}",
        "deposit_percent": f"{order.promotion.deposit_percent}",
        "can_pay_deposit": order.status == Order.APPROVED,
        "can_pay_full": Order.APPROVED <= order.status <= Order.DEPOSIT_PAID,
        "show_timeline": Order.DEPOSIT_PAID < order.status,
    }
    context["timeline"] = [ order.get_timeline(i) for i in range(Order.DEPOSIT_PAID + 1, Order.COMPLETED+1, 1) ]
    context["title"] = order.product_id

    context["form"] = UploadImageForm()
    context["deposit_form"] = UploadDeposit()

    return render(request, template_name, context)

@login_required
def upload_deposit_view(request, pk):
    order = Order.objects.filter(pk=pk, user=request.user).first()
    if order == None:
        raise Http404
    
    if request.method == "POST":
        form = UploadDeposit(request.POST, request.FILES)
        if form.is_valid():
            order.deposit_image = form.cleaned_data["image"]
            # order.status = Order.DEPOSIT_PAID
            order.save()
            messages.add_message(request, messages.SUCCESS, "อัพโหลดรูปภาพเรียบร้อยแล้ว")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.add_message(request, messages.ERROR, "ไม่สามารถอัพโหลดรูปภาพได้")
            return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def upload_full_view(request, pk):
    order = Order.objects.filter(pk=pk, user=request.user).first()
    if order == None:
        raise Http404
    
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            order.full_image = form.cleaned_data["image"]
            order.address = form.cleaned_data["address"]
            # order.status = Order.COMPLETED_PROCESS
            order.save()
            messages.add_message(request, messages.SUCCESS, "อัพโหลดรูปภาพเรียบร้อยแล้ว")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.add_message(request, messages.ERROR, "ไม่สามารถอัพโหลดรูปภาพได้")
            return redirect(request.META.get("HTTP_REFERER", "/"))
