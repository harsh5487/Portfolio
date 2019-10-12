from django.contrib import admin
from django.urls import path,include

#update

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('app_portfolio.urls')),
]
