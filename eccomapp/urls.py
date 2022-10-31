from django.urls import path
from .views import *

app_name = "eccomapp"
urlpatterns = [

    path('', HomeView.as_view(), name="home"),

    path("register/", RegisterPage.as_view(), name="customerregisteration"),
    path("logout/", CustomerLogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path('profile/', CustomerProfile.as_view(), name="profile"),
    path('profile/order-<int:pk>/',
         CustomerOrderDetailView.as_view(), name="orderdetails"),
    path('profile-update/<int:pk>/',
         ProfileUpdateView.as_view(), name="profile-update"),
    path('createprofile/', CustomerProfileCreateView.as_view(), name="createprofile"),

    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path("all-product/", AllProductsView.as_view(), name="all-product"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("add-to-cart/<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path('mycart/', MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart",),
    path('checkout/', CheckOutView.as_view(), name="checkout"),
    path('success-order/', SuccessOrderView.as_view(), name="ordersucess"),
    path('cancelorder/<int:pk>/', DeleteOrder.as_view(), name="cancelorder"),


]
