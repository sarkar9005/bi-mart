from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, CategoryView, SubcategoryView, brand_cat, BrandDetailView, ProductDetailView, AllCategoriesView, AddToCartView,  logout, CartDetailView, CheckoutFormView, CheckoutView, ProfileView, my_addressbook, CheckPincodeView, SearchView, search_suggestions, OrderView, ClearSearchHistoryView, SendVerificationCodeView, VerifyCodeView, OtpValidate

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<int:val>/', CategoryView.as_view(), name='category'),
    path('brand/<int:brand_id>/', brand_cat, name='brand_cat'),
    path('subcategory/<int:val>/', SubcategoryView.as_view(), name='subcategory'),
    path('brand/<int:brand_id>/', BrandDetailView.as_view(), name='brand_detail'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('all_categories/', AllCategoriesView.as_view(), name='all_categories'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('logout/', logout, name='logout'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('checkout_form/', CheckoutFormView.as_view(), name='checkout_form'),
    path('check_out/', CheckoutView.as_view(), name='check_out'),
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('my_addressbook/', my_addressbook, name='my_addressbook'), 
    path('check_pin/', CheckPincodeView.as_view(), name='my_addressbook'), 
    path('search/', SearchView.as_view(), name='search'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('clear_search_history/', ClearSearchHistoryView.as_view(), name='clear_search_history'),
    path('search_suggestions/', search_suggestions, name='search_suggestions'),
    path('send_code/', SendVerificationCodeView.as_view(), name='send_code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('otpvalidate', OtpValidate.as_view(), name='opt validate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

