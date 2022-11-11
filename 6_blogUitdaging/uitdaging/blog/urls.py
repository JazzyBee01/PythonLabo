from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('monthOverview/<int:month_id>/', views.monthOverview, name='month'),
    path('yearOverview/<int:year>/', views.yearOverview)
]