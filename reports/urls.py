from django.urls import path
from .views import *


app_name = "reports"
urlpatterns = [
    path('', ReportView.as_view(), name="reports"),
    path('customer/', UserReportListView.as_view(), name="customer"),
    path('orders/', OrderReportListView.as_view(), name="orders"),
    path('orderdetail/<int:pk>/',
         OrderReportDetailView.as_view(), name="orderdetail"),
    path('product/', ProductReportListView.as_view(), name="product"),
    path('productcreate/', ProductCreateView.as_view(), name="productcreate"),
    path('productedit/<slug:slug>/',
         ProductReportUpdateView.as_view(), name="productedit"),
    path('productdel/<slug:slug>/',
         ProductDeleteView.as_view(), name="productdel"),
    path('cartproduct/', CartproductListView.as_view(), name="cartproduct"),

]
