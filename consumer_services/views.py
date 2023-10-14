# consumer_services/views.py
from datetime import datetime
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, ServiceRequest
from .forms import RequestStatusUpdateForm, ServiceRequestForm, RequestTrackingForm, UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages



def register_user(request):
    return create_user(request=request, user_type=UserProfile.UserType.USER)


def register_representative(request):
    return create_user(request=request, user_type=UserProfile.UserType.REPRESENTATIVE)


def create_user(request, user_type: UserProfile.UserType):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            profile = UserProfile()
            user = form.save()
            profile.user = user
            profile.user_type = user_type
            profile.save()
            # auth_login(request, user)
            form = UserCreationForm()
            return redirect('login')
    elif request.user and request.user.username:
        return redirect('submit_request')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            userProfile = UserProfile.objects.get(user = form.get_user())

            if userProfile.user_type == userProfile.UserType.USER.value:
                return redirect('track_request')
            else:
                return redirect('representative_dashboard') # return representative dashboard html
    elif request.user and request.user.username:
        userProfile = UserProfile.objects.get(user = request.user)

        if userProfile.user_type == UserProfile.UserType.USER.value:
            return redirect('track_request')
        else:
            return redirect('representative_dashboard') # return representative dashboard html
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def editProfile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()

        forget_password_form = PasswordChangeForm(request.user, request.POST)
        if forget_password_form.is_valid():
            updated_user = forget_password_form.save()
            update_session_auth_hash(request, updated_user)

        return redirect('logout')
    else:
        user_form = UserForm(instance=request.user)
        forget_password_form = PasswordChangeForm(request.user)

    return render(request, 'edit_profile.html', {'user_form' : user_form, 'forget_password_form': forget_password_form})


@login_required
def submit_request(request):
    request_id = ''
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.customer = request.user
            request_obj.request_id = uuid.uuid4()
            request_obj.submission_date = datetime.now()
            request_obj.save()
            request_id = request_obj.request_id
            form = ServiceRequestForm()
            return render(request, 'submit_request.html', {'form': form, 'request_id' : request_id})
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

@login_required
def track_request(request):
    serviceRequests = ServiceRequest.objects.filter(customer=request.user.id)
    if request.method == 'POST':
        form = RequestTrackingForm(request.POST)
        if form.is_valid():
            request_id = form.cleaned_data['request_id']
            service_request = ServiceRequest.objects.get(request_id=request_id)
            return render(request, 'track_request.html', {'service_request': service_request, 'service_requests': serviceRequests})
    else:
        form = RequestTrackingForm()
    return render(request, 'track_request.html', {'form': form, 'service_requests': serviceRequests})


@login_required
def representative_dashboard(request):
    choices = ServiceRequest.ServiceRequestStatus.choices
    if request.method == 'POST':
        print('body', request.body)
        print(request.POST['request_status'])
        request_status = request.POST['request_status']
        request_id = request.POST['request_id']
        service_request = ServiceRequest.objects.get(request_id=request_id)
        service_request.request_status = request_status
        service_request.resolution_date = datetime.now()
        service_request.save()
        serviceRequests = ServiceRequest.objects.all()
        for a in serviceRequests:
            print(a.request_status)
        return render(request, 'representative_dashboard.html', {'choices':choices, 'service_requests': serviceRequests})
    else:
        pass
    
    serviceRequests = ServiceRequest.objects.all()
    print(choices)
    return render(request, 'representative_dashboard.html', {'choices':choices, 'service_requests': serviceRequests})