"""
URL configuration for dorzi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/tailor/<int:tailor_id>/', views.tailor_api, name='tailor_api'),
    path('admin/', admin.site.urls,name='iloveu'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('findTailor/', views.findTailor, name='findTailor'),
    path('pre-Designed/', views.pre_designed, name='pre_designed'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='user_signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.customer, name='customer'),
    path('updateuser/', views.updateuser, name='updateuser'),
    path('deleteuser/', views.delete_user, name='deleteuser'),
    path('accounts/', include('allauth.urls')),
    path('update-measurements/', views.update_measurements, name='update_measurements'),
    path('tailor-update-measurements/', views.tailor_update_measurements, name='tailor_update_measurements'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
    path('update-timeline-date/', views.update_timeline_date, name='update_timeline_date'),
    
    #------------------------------------------
    # Order Management
    path('create_order/',views.create_order, name='create_order'),
    
    
    #-------------------------------------------
    # Custuom Order Management
    path('create-custom-orders/<int:tailor_id>/', views.create_custom_orders, name='create_custom_orders'),
    
    
    #------------------------------------------
    path('tailor_signup/', views.tailor_signup, name='tailor_signup'),
    path('tailorDeshboard/', views.tailor_dashboard, name='tailor_dashboard'),
    path('tailor_login/', views.tailor_login, name='tailor_login'),
    path('tailor_detail/', views.tailor_details, name='tailor_details'),
    path('updateTailor/',views.updatetailor,name='updatetailor'),
    path('deleteTailor/',views.deletetailor,name='deletetailor'),
    
    #-------------------------------------------
    
    path('createreviews/',views.createreviews,name='createreviews'),
    path('deletereviews/',views.deletereviews,name='deletereviews'),
    path('updatereviews/',views.updatereviews,name='updatereviews'),
    
    #--------------------------------------------
    
    path('addDress/', views.addDress, name='addDress'),
    path('get-dress-details/<int:product_id>/', views.get_dress_details, name='get_dress_details'),
    
    #-------------------------------------------
    
    path('addEmbroidery/',views.addEmbroidery, name = 'addEmbroidery'),
    path('get-embroidery-details/<int:embroidery_id>/', views.get_embroidery_details, name='get_embroidery_details'),
    
    #-------------------------------------------
    
    path('favorites/toggle/<int:tailor_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_tailors, name='favorite_tailors'),
    
    #-------------------------------------------
    
    # Password Reset
    path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"), 
         name="password_reset"),
    
    path("password_reset_done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), 
         name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    
    path("password_reset_complete/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"), 
         name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
