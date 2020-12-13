from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, TemplateView, UpdateView

from hikemuch_auth.forms import RegisterForm, ProfileForm, LoginForm, EditProfileForm
from hikemuch_auth.models import UserProfile


@transaction.atomic
def register_user(request):
    if request.method == 'GET':
        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }

        return render(request, 'auth/register.html', context)
    else:
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('index')

        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }

        return render(request, 'auth/register.html', context)
#
# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'auth/register.html'
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['user_form'] = context['form']
#         context['profile_form'] = ProfileForm()
#
#         return context

@transaction.atomic
def register_user(request):
    if request.method == "GET":
        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }
        return render(request, 'auth/register.html', context)
    else:
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        #pravim register i vednaga logvame potrebitel
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #commit-False se izpolzva kato defferva zapazvaneto. kato rezultat se vrushta gotov profil obekt kojto ne se zapazva.
            profile = profile_form.save(commit=False)
            #taka se navryzvat user s profil
            profile.user = user
            profile.save()

            #tuk se izpolzvat transacii. ili vsichki operacii ili nito edna.
            login(request, user)
            return redirect('index')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'auth/register.html', context)





def get_redirect_url(params):
    redirect_url = params.get('return_url')
    return redirect_url if redirect_url else 'index'


def login_user(request):
    if request.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }

        return render(request, 'auth/login.html', context)
    else:
        login_form = LoginForm(request.POST)

        return_url = get_redirect_url(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(return_url)

        context = {
            'login_form': login_form,
        }

        return render(request, 'auth/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')


def edit_profile(request):
    form = ProfileForm(instance=request.user)
    args = {'form': form}
    return render(request, 'auth/edit_profile.html', args)


def edit_user(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('show profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'auth/edit_profile_page.html', args)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('show profile')
        return redirect('auth/change_password.html')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'auth/change_password.html', args)



def profile(request, pk=None):
    user = request.user if pk is None else User.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'profile_user': user,
            'profile': user.userprofile,
            'hikes': user.hike_set.all(),
            'form': ProfileForm(),
        }

        return render(request, 'auth/profile.html', context)

    else:
        form = ProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('show profile')

        return redirect('show profile')


    # args = {'user': request.user}
    # return render(request, 'auth/profile')



# class EditProfileView(generic.UpdateView):
#     model = UserProfile
#     template_name = 'auth/edit_profile_page.html'
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#
#         context['user_form'] = context['form']
#         context['profile_form'] = ProfileForm()
#
#         return context




#
# class EditProfilePageView(generic.UpdateView):
#     model = UserProfile
#     template_name = 'auth/edit_profile_page.html'
#     fields = ['username', 'password', 'date_of_birth', 'profile_image']
#     success_url = reverse_lazy('index')
#
#
#
# class ShowProfilePageView(generic.ListView):
#     pass
#
#
#




# class RegisterView(TemplateView):
#     template_name = 'auth/register.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_form'] = RegisterForm()
#         context['profile_form'] = ProfileForm()
#         return context
#
#     @transaction.atomic
#     def post(self, request):
#         user_form = RegisterForm(request.POST)
#         profile_form = ProfileForm(request.POST, request.FILES)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#
#             login(request, user)
#             return redirect('index')
#
#         context = {
#             'user_form': RegisterForm(),
#             'profile_form': ProfileForm(),
#         }
#
#         return render(request, 'auth/register.html', context)
#