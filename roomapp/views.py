from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from roomapp.forms import SignUpForm, UserForm, ProfileForm, RoomCreateForm
from roomapp.models import Profile, Room
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.urls import reverse
from django.views.generic import CreateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.user,"=============")
        if form.is_valid():
            post = form.save(commit=False)
            if not request.user.is_anonymous:
                post.has_room_admin = request.user
                room_inst = Room.objects.get(user=post.has_room_admin)
                if room_inst:
                    post.room = room_inst
                    post.save()
                post.save()
                return redirect('home')
            
            post.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@transaction.atomic
def home(request):
    if request.user.has_room_admin or request.user.room:
        return redirect(reverse('view_room'))
    if not request.user.has_room_admin and not request.user.room:
        return redirect(reverse('create_room'))

    return render(request, 'home.html', {})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'), extra_tags='alert')
            return redirect('/update-profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/updateprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def create_room(request):
    if request.method == 'POST':
        if request.user.has_room_admin:
            messages.success(request, _('only ADMIN has permissions to create a room'), extra_tags='alert')
            return redirect(reverse('view_room'))
        room_inst = Room.objects.get(user=request.user)
        print(room_inst,"pppppp   create_room   ppppppppp")
        if room_inst:
            messages.success(request, _('Room was successfully created!'), extra_tags='alert')
            return redirect(reverse('view_room'))

        room_form = RoomCreateForm(request.POST)
        if room_form.is_valid():
            post = room_form.save(commit=False)
            post.user = request.user
            post.save()
            user_inst = User.objects.get(email=request.user.email)
            user_inst.room = post
            user_inst.save()
            messages.success(request, _('Room was successfully created!'), extra_tags='alert')
            return redirect(reverse('view_room'))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        room_form = RoomCreateForm()
    return render(request, 'room/create_room.html', {'room_form': room_form})


@method_decorator(login_required, name='dispatch')
class RoomsView(generic.ListView):
    context_object_name = 'room_details'
    template_name = 'room/view_room.html'
    
    def get_queryset(self):
        queryset = Room.objects.filter(user=self.request.user)#get(user=request.user)
        return queryset

class DisplayUsersView(generic.ListView):
    # model = User
    context_object_name = 'user_list'
    template_name = 'profiles/display_users.html'

    def get_queryset(self):
        if self.request.user.has_room_admin:
            queryset = User.objects.filter(has_room_admin=self.request.user.has_room_admin)
        else:
            queryset = User.objects.filter(has_room_admin=self.request.user)
        
        return queryset

class ProfileView(generic.ListView):
    model = Profile
    context_object_name = 'user_profile'
    queryset = Profile.objects.all()
    template_name = 'profiles/profile.html'

    # def get_queryset(self):
    #     queryset = Profile.objects.filter(user=self.request.user.has_room_admin)[0]#get(user=request.user)
    #     return queryset

class ManageRecords(View):

    def get(self, request):
        print("ttttttttttttt")
        return render(request, 'room/create_room.html', {'room_form': room_form})

    def post(self, request):
        print("rrrrrrrrr")
        return render(request, 'room/create_room.html', {'room_form': room_form})

    def put(self, request):
        print("yyyyyyyyyyy")
        return render(request, 'room/create_room.html', {'room_form': room_form})

    def delete(self, request):
        print("uuuuuuuuuuuuuu")
        return render(request, 'room/create_room.html', {'room_form': room_form})
