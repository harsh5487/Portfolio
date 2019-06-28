from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('stocks/', views.stocks, name='stocks'),
    path('details/<slug:slug>', views.details, name='details'),
    path('get_data/<slug:slug>', views.get_data, name='get_data'),
    path('delete/<slug:slug>' , views.delete, name='delete'),
    path('edit/<slug:slug>' , views.edit, name='edit'),
    path('balance_sheet_data/' , views.balance_sheet_data, name='balance_sheet_data'),
    path('balance_sheet/' , views.balance_sheet, name='balance_sheet'),
    path('sell/<slug:slug>' , views.sell, name='sell'),
    path('500_server_error/' , views.server_error, name='500'),
 #   path('name/', views.get_name, name='get_name'),
]

if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
