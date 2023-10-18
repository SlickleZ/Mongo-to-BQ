from django.urls import path
from . import  views


urlpatterns = [
    path('', views.index, name='index'),
    path("rand_number/<str:user_name>", views.rand_number_and_save, name="rand_number_and_save"),
    path("preference/<str:user_name>&<str:lottery_number>&<str:preference>", views.like_and_dislike, name="like_and_dislike"),
]
