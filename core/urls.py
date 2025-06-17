from django.urls import path
from . import views


urlpatterns=[
    
    path('', views.home, name='home'),
    path('user/profile/', views.user, name='user_profile'),
    path('user/notifications/', views.notifications, name='notifications'),
    path('user/dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name= 'signup'),
    path('login/', views.login, name='login'),
    
    
    path('user/data/', views.data, name='data'),
    path('user/data/type/', views.datatype, name='datatype'),
    path('user/data/plan/', views.dataplan, name='dataplan'),
    path('user/data/buy-data/', views.buy_data, name='buy_data'),
    
    
    path('user/airtime/', views.airtime, name='airtime'),
    path('user/verify-phone/', views.verify_phone, name='verify_phone'),
    path('user/verify-phone-no/', views.verify_airtime_phone, name='verify_airtime_phone'),
    path('user/buy-airtime/', views.buy_airtime, name='buy_airtime'),
    path('user/airtime/type/', views.fetch_type, name='fetch_type'),
    path('user/airtime/amount/', views.fetch_amount, name='fetch_amount'),
    
    
    path('user/cable/', views.cable, name='cable'),
    path('user/cable/plan/', views.cableplan, name='cableplan'),
    path('user/cable/verify-cable/', views.verify_cable, name='verify_cable'),
    path('user/cable/buy-cable/', views.buy_cable, name='buy_cable'),
    
    
    path('user/electricity/', views.electricity, name='electricity'),
    path('user/buy-electricity/', views.buy_electricity, name='buy_electricity'),
    
    path('user/logout/', views.logout, name='logout'),
    path('user/password/', views.password, name='password'),
    #path('user/change-password', views.change_password, name='change_password'),
    
    path('user/transactions/', views.transaction, name='transactions'),
    path('user/transaction/detail/<int:pk>', views.transaction_detail, name='transaction_detail'),
    path('user/transaction/success/', views.success, name='success'),
    
    
    path('user/pin/', views.pin, name='pin'),
    path('user/pin/create-pin/', views.create_pin, name='create_pin'),
    path('user/pin/update-pin/', views.update_pin, name='update_pin'),
    
    
    path('funding/', views.funding, name='funding'),
    path('funding/bank-transfer/', views.bank_transfer, name='bank_transfer'),
    path('funding/manual-funding/', views.manual_funding, name='manual_funding'),
    path('funding/card-payment/', views.card, name='card'),
    path('funding/payment/', views.payment, name='payment'),
    

    path('user/upgrade-package/', views.upgrade, name='upgrade'),
    
    path('monify/webmaster/upme/', views.monify_update, name='monify_upme'),
    path('new/stack/update/', views.paystack_update, name='pay_stack_upme'),
    path('admin/', views.admin, name='admin'),
    path('super-admin/', views.admin, name='admin'),
    
    
    path('forget-password/', views.reset_password, name='reset_password'),
    path('email-sent/', views.reset_password_done, name='reset_password_done'),
    path('send-mail/', views.send_mail, name='send_mail'),
]