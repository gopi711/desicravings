"""desicravings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.start1),
    path(r'login/',views.Login),
    path(r'adminMenu/',views.adminMenu),
    path(r'addnewitem/',views.addnewitem),
    path(r'Logout/',views.start1),
    path(r'UpdateItem/',views.UpdateItem),
    path(r'UpdateItemData/',views.UpdateItemData),
    path(r'UpdateItemData/',views.UpdateItemData),
    path(r'DeleteItem/',views.DeleteItem),
    path(r'DeleteItemData/',views.DeleteItemData),
    path(r'cart-items/',views.cartitems),
    path(r'personal_info/',views.personal_info),
    path(r'placeorder/',views.placeorder),
    path(r'track/',views.track),
    path(r'complete-order/',views.completeorder),
    path(r'user-cancel-item/',views.usercancelitem),
    path(r'admin-cancel-item/',views.admincancelitem),
    path(r'track-order/',views.trackorder),
]
