from django.shortcuts import render, redirect, get_object_or_404
from .form import UserLoginForm, UserRegistrationForm, Editprofileform
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from post.models import post
from django.contrib.auth.decorators import login_required
from .models import relation
from django.http import JsonResponse


def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect('post:all_posts')
            else:
                messages.error(request, 'wrong username or password', 'warning')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'you registered successfully', 'success')
            return redirect('posts:all_posts')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'you logged out successfully', 'success')
    return redirect('post:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = post.objects.filter(user=user)
    self_dash = False
    is_following = False
    Relation = relation.objects.filter(from_user=request.user, to_user=user)
    if Relation.exists():
        is_following = True
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html',
                  {'user': user, 'posts': posts, 'self_dash': self_dash, 'is_following': is_following})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = Editprofileform(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'you are edited successfully', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = Editprofileform(instance=user.profile, initial={'email': request.user.email})
    return render(request, 'account/edit_profile.html', {'form': form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            relation(from_user=request.user, to_user=following).save()


@login_required
def unfollow(request):
    if request.user == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexiste'})