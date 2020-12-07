from django.urls import path

from hikemuch_auth.views import login_user, logout_user, RegisterView

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register user'),
    path('login/', login_user, name='login user'),
    path('logout/', logout_user, name='logout user'),
)
