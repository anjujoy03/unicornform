from django.urls import path
from . import views
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('sign_up', views.SaveCustomer, name='sign_up'),
  path('auth', views.Authenticate, name='auth'),
  path('orders', views.AddCustomerordes, name='orders'),
  # path('save_supplier', views.SaveSupplier.as_view(), name='save_supplier'),
  path('save_machniries', views.SaveMachiners, name='save_machniries'),
  path('save_labours', views.SaveLabours, name='save_labours'),
  path('save_categories', views.saveCategories.as_view(), name='save_categories'),
  path('get_categories', views.getCategories, name='get_categories'),
  path('stock_based_list', views.getStockBasedList.as_view(), name='stock_based_list'),
  path('supplier_save', views.SaveSupplier, name='supplier_save'),
  path('temp_dtls', views.SaveSuppliertempdetails, name='temp_dtls'),
  path('prod_dtls_save', views.prod_dtls_save, name='prod_dtls_save'),
  path('delete_prod_dtls', views.delete_prod_dtls, name='delete_prod_dtls'),
  path('getlabours_technisions_list', views.getlabours_technisions_list, name='getlabours_technisions_list'),
  path('getmachneries_spareparts_list', views.getmachneries_spareparts_list, name='getmachneries_spareparts_list'),
  path('csrftokens', views.csrftokens, name='csrftokens'),
  path('get_prod_list',views.get_prod_list,name='get_prod_list'),
  path('prod_list_byid',views.prod_list_byid,name='prod_list_byid'),
  path('supplier_list',views.supplier_list,name='supplier_list'),
  path('prod_list_cat',views.prod_list_cat,name='prod_list_cat'),
  path('orders_enquiries',views.orders_enquiries,name='orders_enquiries'),
  path('productSupplideerlst',views.productSupplideerlst,name='productSupplideerlst'),
  path('customer_requirements',views.customer_requirements,name='customer_requirements'),
  path('users_list',views.users_list,name='users_list'),
  path('supplier_details',views.supplier_details,name='supplier_details'),
  path('accept_supplier',views.accept_supplier,name='accept_supplier'),

  

  
  
  



  



  
  
  

  
  
  
  


  
  

  
  


  

  
  
  
  
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
