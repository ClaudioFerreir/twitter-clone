from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Twitter
from .forms import TwitterForm, SignupForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TwitterForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                twitter = form.save(commit=False)
                twitter.user = request.user
                twitter.save()
                messages.success(request, 'Your Twitter Has Been Posted!')
                return redirect('home')

        twitters = Twitter.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"twitters": twitters, "form": form})
    else:
        twitters = Twitter.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"twitters": twitters})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You Must Be Logged In To View this Page')
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        twitters = Twitter.objects.filter(user_id=pk).order_by('-created_at')

        # Post Form logic
        if request.method == "POST":
            # Get current user ID
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()


        return render(request, 'profile.html', {'profile': profile, 'twitters': twitters})
    else:
        messages.success(request, 'You Must Be Logged In To View this Page')
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In! Get TWITTERING!')
            return redirect('home')
        else:
            messages.success(request, 'There is a error logging in. Please Try Again!')
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You Have Been Logged Out!')
    return redirect('home')

def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome!')
            return redirect('home')

    return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id=request.user.id)
        # Get Forms
        user_form = SignupForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, 'You Profile Has Been Updated!')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, 'You Must Be Logged In To View this Page!')
        return redirect('home')

