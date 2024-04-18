from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('allproducts', views.allproducts, name='allproducts'),
    path('service', views.service, name='service'),
    path('orderh', views.orderh, name='orderh'),

    path('about/', views.about, name='about'),
    path('personal/', views.personal, name='personal'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),

    path('product/<int:pk>', views.product, name='product'),
    path('personal1/<int:pk>', views.personal1, name='personal1'),

    path('order/<int:pk>/', views.order, name='order'),

    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name="reset_password"),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='reset_confirm.html'),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name="password_reset_complete",
    ),

    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_payment_link/', views.create_payment_link, name='create_payment_link'),
    #path('create/', views.create_cproduct, name='create_cproduct'),
    path('create_order/', views.create_order, name='create_order'),
    path('save-data/', views.save_data, name='save_data'),
    path('save_quote/', views.save_quote, name='save_quote'),


    path('fetch_product_id/', views.fetch_product_id, name='fetch_product_id'),

    



]
