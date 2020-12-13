from django.urls import path

from hikemuch_auth.views import login_user, logout_user, edit_profile, edit_user, change_password, \
    profile, register_user

# ShowProfilePageView, EditProfilePageView edit_profile EditProfileView, RegisterView

urlpatterns = (
    # path('register/', RegisterView.as_view(), name='register user'),
    path('register/', register_user,  name='register user'),
    path('login/', login_user, name='login user'),
    path('logout/', logout_user, name='logout user'),
    path('edit_profile/', edit_profile, name='edit profile'),
    path('edit_user/', edit_user, name='edit user'),
    path('change_password/', change_password, name='change password'),
    path('profile', profile, name='show profile'),
    path('profile/<int:pk>/', profile, name='show user profile'),
)
