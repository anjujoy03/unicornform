from django.urls import path
from . import views
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('sign_up', views.SaveCustomer.as_view(), name='sign_up'),
  path('auth', views.Authenticate.as_view(), name='auth'),
  path('orders', views.AddCustomerordes.as_view(), name='orders'),
  # path('save_supplier', views.SaveSupplier.as_view(), name='save_supplier'),
  path('save_machniries', views.SaveMachiners.as_view(), name='save_machniries'),
  path('save_labours', views.SaveLabours.as_view(), name='save_labours'),
  path('save_categories', views.saveCategories.as_view(), name='save_categories'),
  path('get_categories', views.getCategories.as_view(), name='get_categories'),
  path('stock_based_list', views.getStockBasedList.as_view(), name='stock_based_list'),
  path('supplier_save', views.SaveSupplier.as_view(), name='supplier_save'),
  path('temp_dtls', views.SaveSuppliertempdetails.as_view(), name='temp_dtls'),
  path('prod_dtls_save', views.prod_dtls_save.as_view(), name='prod_dtls_save'),
  path('delete_prod_dtls', views.delete_prod_dtls.as_view(), name='delete_prod_dtls'),
  path('getlabours_technisions_list', views.getlabours_technisions_list.as_view(), name='getlabours_technisions_list'),
  path('getmachneries_spareparts_list', views.getmachneries_spareparts_list.as_view(), name='getmachneries_spareparts_list'),
  
  


  
  

  
  


  

  
  
  
  
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
