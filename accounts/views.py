from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_action, authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from accounts.forms import UserChangeForm, UserCreationForm
from order.models import Order


def is_logged(request):
    if request.user.is_authenticated:
        return True
    return False


def get_user(request):
    if request.method == 'POST':
        data = dict()
        if request.user.is_authenticated:
            user = request.user
            data['user'] = model_to_dict(user, exclude=['avatar'])
            data['user']['display_name'] = user.full_name
            data['user']['get_complete_name'] = user.get_complete_name
            data['user']['account_url'] = reverse('account')
        else:
            data['user'] = None
        return JsonResponse(data)
    return HttpResponseNotFound()


def account(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')

    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('/account')
        else:
            context = {
                'user': user,
                'form': form
            }
            return render(request, 'registration/account.html', context)

    else:
        form = UserChangeForm(instance=user)
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'registration/account.html', context)


def log_in(request):

    if is_logged(request):
        return redirect('/account')

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/account')

    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


def log_out(request):
    logout_action(request)
    return redirect('/account/login')


def registration(request):

    if is_logged(request):
        return redirect('/account')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/account')

    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account')
        else:
            context = {
                'form': form
            }
            return render(request, 'registration/change_password.html', context)

    form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'registration/change_password.html', context)


def my_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()
    orders = Order.objects.filter(user_id=request.user.id).order_by('-timestamp')
    if not orders:
        return redirect('catalog_page', slug='cases')
    context = {
        'orders': orders
    }
    return render(request, 'order/my_orders.html', context)
