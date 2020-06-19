from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.StoreView.as_view(), name="store"),
    path('cart/', views.cart.as_view(), name='cart'),
    path('myorder/', views.myorder.as_view(), name='myorder'),
    path('success/', views.success, name='success'),
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/',
         views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),




    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset.html'),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='rpassword_reset_complete.html'),
         name='password_reset_complete'),


    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout')

]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
