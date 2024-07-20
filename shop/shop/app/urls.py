from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, CategoryView, SubcategoryView, ProductDetailView, AllCategoriesView, AddToCartView,  logout, CartDetailView, CheckoutFormView, CheckoutView, ProfileView, my_addressbook, CheckPincodeView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<int:val>/', CategoryView.as_view(), name='category'),
    path('subcategory/<int:val>/', SubcategoryView.as_view(), name='subcategory'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('all_categories/', AllCategoriesView.as_view(), name='all_categories'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('logout/', logout, name='logout'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('checkout_form/', CheckoutFormView.as_view(), name='checkout'),
    path('check_out/', CheckoutView.as_view(), name='check_out'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('my_addressbook/', my_addressbook, name='my_addressbook'), 
    path('check_pin/', CheckPincodeView.as_view(), name='my_addressbook'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
