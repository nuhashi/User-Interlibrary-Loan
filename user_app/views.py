from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Tambah ini
from .models import Order
from .forms import OrderForm

def home(request):
    return render(request, 'home.html')

@login_required # Hanya user login boleh masuk dashboard
def dashboard(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user # Automatik ikat request dengan user login
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    
    # Filter: Hanya tunjuk order kepunyaan user yang sedang login sahaja
    orders = Order.objects.filter(user=request.user) 
    return render(request, 'dashboard.html', {'orders': orders, 'form': form})

@login_required
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user) # Pastikan user delete kepunyaan sendiri sahaja
    order.delete()
    return redirect('dashboard')
from django.contrib.auth.forms import UserCreationForm # Tambah import ni kat atas sekali
from django.contrib import messages # Tambah ni juga

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})