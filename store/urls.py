from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home / Login / Logout
    path("", views.store, name='store'),
    path("account/login/", auth_views.LoginView.as_view(), name='login' ),
    path("logout/", views.log_out, name="logout"),
    # Cart
    path("cart/", views.cart, name='cart'),
    # Checkout
    path("checkout/", views.checkout, name='checkout'),
    # Secondary Links
    path("update_item/", views.updateItem, name='update_item'),
    path("process_order/", views.processOrder, name='process_order'),
    # Add New/Update/Delete Product
    path("inventory/new", views.AddProductView.as_view(), name='add_product'),
    path("inventory/edit/<slug:pk>", views.UpdateProductView.as_view(), name='edit_product'),
    path('inventory/delete/<slug:pk>', views.DeleteProductView.as_view(), name="delete_product"),
    path('product/<slug:pk>', views.ViewProductPage.as_view(), name='view_product'),
]
