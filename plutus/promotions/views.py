from django.shortcuts import render

def all_deals_view(request):
    template_name = "promotions/promotion_list.html"
    context = {"title": "ALL DEALS!"}
    return render(request, template_name, context)
