from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from ..forms.user_forms import RegisterForm, EditUserForm
from ..models import League, Team

def user_profile(request, user_id):
    view_user = get_object_or_404(User, id=user_id)
    leagues = League.objects.filter(created_by=view_user).order_by("name")
    teams = Team.objects.filter(created_by=view_user).order_by("name")

    context = {
        "view_user" : view_user,
        "leagues" : leagues,
        "teams" : teams
    }

    return render(request, "rpiapp/user_profile.html", context)

@login_required
def edit_profile(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)
    update_form = EditUserForm(instance=user_instance)
    password_reset_form = PasswordChangeForm(user_instance)
    if request.user == user_instance:
        if request.method == 'POST':
            if 'update_fields' in request.POST:
                update_form = EditUserForm(request.POST, instance=user_instance)
                if update_form.is_valid():
                    update_form.save()
                    messages.success(request, "Profile changed successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if 'password_change' in request.POST:
                password_reset_form = PasswordChangeForm(user_instance, request.POST)
                if password_reset_form.is_valid():
                    user = password_reset_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Password updated successfully")
                    return HttpResponseRedirect(reverse("rpiapp:index"))
    else:
        messages.error(request,"You cannot edit this profile")
        return HttpResponseRedirect(reverse('rpiapp:user_profile', args=[user_instance.id]))

    context = {
        "update_form" : update_form,
        "password_reset_form" : password_reset_form,
        "user_instance" : user_instance
    }
    return render(request, "registration/edit_profile.html", context)

@login_required
def delete_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user == user:
        user.is_active = False
        user.save()
        messages.success(request, "Account deleted successfully")
        return HttpResponseRedirect(reverse('rpiapp:index'))
    
    else:
        messages.error(request, "You cannot delete this account")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def register_user(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('rpiapp:index'))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form" : form })

def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('rpiapp:index'))
    else:
        form = AuthenticationForm()
    
    return render(request, "registration/login.html", {"form" : form})

def logout_user(request):
    logout(request)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
