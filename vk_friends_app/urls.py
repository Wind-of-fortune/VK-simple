from django.urls import path
from vk_friends_app.views import *


urlpatterns = [
    path('', first_view, name='first_view'),
    path('friends', friends_list, name='friends_list')
]
