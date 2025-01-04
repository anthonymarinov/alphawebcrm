from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('crm_home/', views.crm_home, name='crm_home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('record/<int:pk>', views.client_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('captcha/', include('captcha.urls')),
]
