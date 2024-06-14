from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/followers/<int:pk>/', views.followers, name='followers'),
    path('profile/follows/<int:pk>/', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('twitter_like/<int:pk>', views.twitter_like, name='twitter_like'),
    path('twitter_show/<int:pk>', views.twitter_show, name='twitter_show'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('delete_twitter/<int:pk>', views.delete_twitter, name='delete_twitter'),
    path('edit_twitter/<int:pk>', views.edit_twitter, name='edit_twitter'),
    path('search', views.search, name='search'),
]
