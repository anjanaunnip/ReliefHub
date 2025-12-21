from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),   # ✅ unified register
    path('login/', views.user_login, name='login'),

    path('donourdashboard/', views.donourdashboard, name='donourdashboard'),
    path('campdashboard/', views.campdashboard, name='campdashboard'),

    path('logout/', views.custom_logout, name='logout'),
    path('donate/categories/', views.donation_categories, name='donation_categories'),
    path('donate/categories/<int:cat_id>/', views.select_donation_item, name='select_donation_item'),
    path('donate/item/<int:item_id>/', views.donation_details, name='donation_details'),
    path('donate/thankyou/', views.donation_thankyou, name='donation_thankyou'),

    path("campdashboard/my_requests/", views.my_requests, name="my_requests"),
    path("campdashboard/new_requests/", views.new_requests, name="new_requests"),
    path("reliefcamp_thankyou/", views.reliefcamp_thankyou, name="reliefcamp_thankyou"),

    # ✅ New URLs for donor notifications
    path("donate/from_request/<int:req_id>/", views.donate_from_request, name="donate_from_request"),
    path("paynow/<int:req_id>/", views.pay_now, name="pay_now"),
    path("payment/success/", views.payment_success, name="payment_success"),

]
