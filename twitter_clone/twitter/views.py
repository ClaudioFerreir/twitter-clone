from django.shortcuts import render, redirect, get_object_or_404
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


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, f'You Have Successfully Unfollowed {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, 'You Must Be Logged In To View this Page')
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, f'You Have Successfully Followed {profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))

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


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles': profiles})
        else:
            messages.success(request, "That's Not Your Profile Page...")
            return redirect('home')
    else:
        messages.success(request, 'You Must Be Logged In To View this Page')
        return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles': profiles})
        else:
            messages.success(request, "That's Not Your Profile Page...")
            return redirect('home')
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


def twitter_like(request, pk):
    if request.user.is_authenticated:
        twitter = get_object_or_404(Twitter, id=pk)
        if twitter.likes.filter(id=request.user.id):
            twitter.likes.remove(request.user)
        else:
            twitter.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You Must Be Logged In To View this Page!')
        return redirect('home')


def twitter_show(request, pk):
    twitter = get_object_or_404(Twitter, id=pk)
    if twitter:
        return render(request, 'show_twitter.html', {'twitter': twitter})
    else:
        messages.success(request, 'That Twitter Does Not Exist!')
        return redirect('home')


def delete_twitter(request, pk):
    if request.user.is_authenticated:
        twitter = get_object_or_404(Twitter, id=pk)
        # Check to see if you own the meep
        if request.user.username == twitter.user.username:
            # Delete the twitter
            twitter.delete()

            messages.success(request, 'The Twitter Has Been Deleted!')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "You Don't Own That Twitter Account!")
            return redirect('home')
    else:
        messages.success(request, 'Please Login To View this Page!')
        return redirect(request.META.get('HTTP_REFERER'))

def edit_twitter(request, pk):
    if request.user.is_authenticated:
        # Grab The Twitter
        twitter = get_object_or_404(Twitter, id=pk)
        # Check to see if you own the meep
        if request.user.username == twitter.user.username:
            form = TwitterForm(request.POST or None, instance=twitter)
            if request.method == 'POST':
                if form.is_valid():
                    twitter = form.save(commit=False)
                    twitter.user = request.user
                    twitter.save()
                    messages.success(request, 'Your Twitter Has Been Edited!')
                    return redirect('home')
            else:
                return render(request, 'edit_twitter.html', {'form': form, 'twitter': twitter})

        else:
            messages.success(request, "You Don't Own That Twitter Account!")
            return redirect('home')
    else:
        messages.success(request, 'Please Login To View this Page!')
        return redirect('home')


def search(request):
    if request.method == 'POST':
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = Twitter.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search.html', {})


def search_user(request):
    if request.method == 'POST':
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})