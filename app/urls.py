from re import template
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import CustomerLoginForm,CustomerChangePassword
urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('prapi',views.ProductAPI),
    path('prapi/<int:pk>',views.ProductAPI),

    path('product_detail/<int:pk>',views.Product_details.as_view(),name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('changepassword/',auth_view.PasswordChangeView.as_view(template_name="app/changepassword.html",
    form_class=CustomerChangePassword,success_url='/passwordchangedone/'),name='changepassword'),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/PasswordChangedone.html'),
    name='passwordchangedone'),
    
    path('mobile/', views.mobile, name='mobile'),

    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    
    path('accounts/login/',auth_view.LoginView.as_view(template_name="app/login.html",
    authentication_form=CustomerLoginForm),name='login'),

    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/',views.CustomerRegistrationview.as_view(),name="customerregistration"),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/',views.payementdone),
    path('password-reset/',auth_view.PasswordResetView.as_view(),name='password-reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
