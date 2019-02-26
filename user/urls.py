from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('app_collection/<str:info>/', views.app_collection, name='app_collection'),
    path('show_collection/', views.show_collection, name='show_collection'),
    path('change_nikename/', views.change_nikename, name='change_nikename'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_code/', views.send_code, name='send_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
