from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from notifications.models import Notification


@login_required
@csrf_exempt
def notification_list_apiview(request):
    notification_qs = request.user.notification_set.filter(read=False).all()
    print(timezone.localtime())
    res_data = {
        "message": {
            "notifications": [{
                "pk": noti.id,
                "title": noti.title,
                "message": noti.message,
                "time": timezone.localtime(noti.created_at).strftime("%d/%m/%Y - %H:%M"),
                "url": reverse("notifications:read_notification", kwargs={"pk": noti.id}),
            } for noti in notification_qs],
        }
    }
    return JsonResponse(
        res_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@login_required
def read_notification_view(request, pk):
    noti = Notification.objects.filter(pk=pk, user=request.user).first()
    if noti is None:
        raise Http404
    noti.read = True
    noti.save()
    return redirect(noti.url)
