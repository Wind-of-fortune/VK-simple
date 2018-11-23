from django.contrib import admin
from django.urls import path
from django.urls import include

from vk_friends_app import urls as vk_friends_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((vk_friends_urls, 'vk_friends_app'), namespace='friends')),
]
