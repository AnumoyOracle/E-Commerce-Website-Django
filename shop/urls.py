from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='Shop_Home'),
    path('about/', views.about,name="About_Us"),
    path('contact/', views.contact,name="Contact_Us"),
    path('tracker/', views.tracker,name="Tracking_Status"),
    path('search', views.search,name="Search"),
    path('products/<int:id>', views.productView,name="Product_View"),
    path('checkout/', views.checkout,name="Checkout"),
    path('update-payment-status/', views.updatePaymentStatus, name='Update_Payment_Status'),
]