from . import views
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

urlpatterns = [
  url(r'sign_up', views.SaveCustomer, name='sign_up'),
  url(r'auth', views.Authenticate, name='auth'),
  url(r'orders', views.AddCustomerordes, name='orders'),
  # path('save_supplier', views.SaveSupplier.as_view(), name='save_supplier'),
  url(r'save_machniries', views.SaveMachiners, name='save_machniries'),
  url(r'save_labours', views.SaveLabours, name='save_labours'),
  url(r'save_categories', views.saveCategories.as_view(), name='save_categories'),
  url(r'get_categories', views.getCategories, name='get_categories'),
  url(r'stock_based_list', views.getStockBasedList.as_view(), name='stock_based_list'),
  url(r'supplier_save', views.SaveSupplier, name='supplier_save'),
  url(r'temp_dtls', views.SaveSuppliertempdetails, name='temp_dtls'),
  url(r'prod_dtls_save', views.prod_dtls_save, name='prod_dtls_save'),
  url(r'delete_prod_dtls', views.delete_prod_dtls, name='delete_prod_dtls'),
  url(r'getlabours_technisions_list', views.getlabours_technisions_list, name='getlabours_technisions_list'),
  url(r'getmachneries_spareparts_list', views.getmachneries_spareparts_list, name='getmachneries_spareparts_list'),
  # path('csrftokens', views.csrftokens, name='csrftokens'),
  url(r'get_prod_list',views.get_prod_list,name='get_prod_list'),
  url(r'prod_list_byid',views.prod_list_byid,name='prod_list_byid'),
  url(r'supplier_list',views.supplier_list,name='supplier_list'),
  url(r'prod_list_cat',views.prod_list_cat,name='prod_list_cat'),
  url(r'bulk_enquiries',views.orders_enquiries,name='bulk_enquiries'),
  url(r'productSupplideerlst',views.productSupplideerlst,name='productSupplideerlst'),
  url(r'customer_requirements',views.customer_requirements,name='customer_requirements'),
  url(r'users_list',views.users_list,name='users_list'),
  url(r'supplier_details',views.supplier_details,name='supplier_details'),
  url(r'accept_supplier',views.accept_supplier,name='accept_supplier'),
  url(r'getProfile',views.getProfile,name='getProfile'),
  url(r'mail',views.Email,name='mail'),
  url(r'Edit_profile',views.Edit_profile,name='Edit_profile'),
  url(r'save_profile',views.save_profile,name='save_profile'),
  url(r'quotaton_form',views.quotaton_form,name='quotaton_form'),
  url(r'quote_list',views.quote_list,name='quote_list'),
  url(r'get_qouteditem',views.get_qouteditem,name='get_qouteditem'),
  url(r'update_quotes',views.update_quotes,name='update_quotes'),
  url(r'buyers_list',views.buyers_list,name='buyers_list'),
  url(r'supdetailslist',views.all_supplier_list,name='supdetailslist'),
  url(r'customer_details',views.customer_details,name='customer_details'),
  url(r'order_details',views.order_details,name='order_details'),
  url(r'quotationlist',views.all_quote_list,name='quotationlist'),
  url(r'pincode',views.pincode,name='pincode'),
  url(r'list_by_id',views.quote_list_by_id,name='list_by_id'),
  url(r'supplierdetails_by_id',views.supplierdetails_by_id,name='supplierdetails_by_id'),
  url(r'customerdetails_by_id',views.customerdetails_by_id,name='customerdetails_by_id'),
  url(r'quotelist_for_all',views.quotelist_for_all,name='quotelist_for_all'),
  url(r'banneraddd',views.banneraddd,name='banneraddd'),
  url(r'addbannerList',views.addbannerList,name='addbannerList'),
  url(r'ImageDetails',views.ImageDetails,name='ImageDetails'),
  url(r'EditBannerImage',views.EditBannerImage,name='EditBannerImage'),
  url(r'deletebanner',views.deletebanner,name='deletebanner'),
  url(r'getOrderdetials',views.getOrderdetials,name='getOrderdetials'),
  url(r'production_details',views.production_details,name='production_details'),
  url(r'getbannerimages',views.getbannerimages,name='getbannerimages'),
  url(r'verifyOTP',views.verifyOTP,name='verifyOTP'),
  url(r'generatebill',views.generatebill,name='generatebill'),
  url(r'getQuotationlist',views.getQuotationlist,name='getQuotationlist'),
  url(r'getAccessories',views.getAccessories,name='getAccessories'),
  url(r'getMachines',views.getMachines,name='getMachines'),
  
  
 
  
  
  

 
  
  
  
  
  
]

