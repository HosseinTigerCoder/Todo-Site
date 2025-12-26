from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_form,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_site,name='logout'),
    path('change-password/',views.change_password,name='change_password'),
    path('change-password-done/',views.change_password_done,name='change_password_done'),
    path('reset_email_sent/',views.send_email_reset,name='reset_email_sent'),
    path('reset_password/<str:token>/',views.reset_form,name='reset_password_form')
]