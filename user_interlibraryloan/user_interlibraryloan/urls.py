from django.contrib import admin
from django.urls import path
from user_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # --- URL UNTUK INTERFACE KAWAN-KAWAN ---
    path('guest/', views.guest_view, name='guest'),
    path('staff/', views.staff_view, name='staff'),
    path('bank/', views.bank_view, name='bank'),
]