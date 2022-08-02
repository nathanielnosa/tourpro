from django.urls import path

from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('overview/<str:id>/', views.overview, name='overview'),
    path('search/', views.search, name='search'),

    path('addtocart/<str:id>/', views.addtocart, name='addtocart'),
    path('myCart/', views.myCart, name='myCart'),
    path('manageCart/<str:id>/', views.manageCart, name='manageCart'),
    path('clearCart/', views.clearCart, name='clearCart'),
    path('checkout/',views.checkout, name='checkout'),
    path('payment/<str:id>/',views.paymentPage, name='payment'),
    path('<str:ref>/',views.verify_payment, name='verify-payment'),
]