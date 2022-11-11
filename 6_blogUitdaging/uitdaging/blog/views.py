from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Post
# Create your views here.
def index(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:10]
    context = {
        'message': "Hello, world. You're at the blog index.",
        'latest_post_list': latest_post_list
        }
    return render(request, 'index.html', context)
def detail(request, post_id):
    response = "Hello, world. You're at the blog detail page of post %s."
    return HttpResponse(response %post_id)
def monthOverview(request, month_id):
    response = "Hello, world. You're at the overview page of month %s."
    return HttpResponse(response %month_id)
def yearOverview(request, year):
    response = "Hello, world. You're at the overview page of year %s."
    return HttpResponse(response %year)

