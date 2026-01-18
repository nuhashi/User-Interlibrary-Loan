from django.contrib import admin
from django.urls import path
from user_app.views import home, dashboard, delete_order, register # Pastikan semua fungsi ini diimport
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]