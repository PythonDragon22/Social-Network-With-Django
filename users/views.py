from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users.forms import User_Signup_Form, User_Signin_Form, UserForm, ProfileForm
from users.models import Profile

# Create your views here.
def registration_page(request):
    return render(request, 'users/registration.html')

class User_Signup_View(View):
    def get(self, request, *args, **kwargs):
        signup_form = User_Signup_Form()
        return render(request, 'users/user_signup.html', context= {'signup_form': signup_form})

    def post(self, request, *args, **kwargs):
        signup_form = User_Signup_Form(request.POST)
        if signup_form.is_valid():
            if signup_form.cleaned_data['password'] and signup_form.cleaned_data['password_confirmation'] and signup_form.cleaned_data['password'] == signup_form.cleaned_data['password_confirmation']:
                if User.objects.filter(email= signup_form.cleaned_data['email']).exists():
                    messages.error(request, 'That email is already taken')
                    return redirect('user_signup_page')

                if User.objects.filter(username= signup_form.cleaned_data['username']).exists():
                    messages.error(request, 'That username is already taken')
                    return redirect('user_signup_page')

                else:
                    new_user = User.objects.create_user(
                        username= signup_form.cleaned_data['username'],
                        email= signup_form.cleaned_data['email'],
                        password= signup_form.cleaned_data['password'],
                    )
                    new_user.first_name = signup_form.cleaned_data['first_name']
                    new_user.last_name = signup_form.cleaned_data['last_name'],
                    new_user.save()
                    messages.success(request, 'You have signed up successfully')
                    return redirect('user_signin_page')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('user_signup_page')
        return render(request, 'users/user_signup.html', context= {'signup_form': signup_form})


class User_Signin_View(View):
    def get(self, request, *args, **kwargs):
        signin_form = User_Signin_Form()
        return render(request, 'users/user_signin.html', context= {'signin_form': signin_form})

    def post(self, request, *args, **kwargs):
        signin_form = User_Signin_Form(request.POST)
        if signin_form.is_valid():
            user = authenticate(username= signin_form.cleaned_data['username'], password= signin_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('user_profile_page')

            else:
                messages.error(request, 'Invalid credentials')
                return redirect('user_signin_page')
        return render(request, 'users/user_signin.html', context= {'signin_form': signin_form})


class User_Signout_View(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You are now logged out')
        return render(request, 'users/user_signout.html')


class UserProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user_id=pk)
        user = profile.user
        user_posts = Post.objects.filter(author=user).order_by('-created_on')

        # Number Of Followers
        followers = profile.followers.all()
        followers_number = len(followers)

        # is_follower = False   == Condition Below
        if len(followers) == 0:
            is_follower = False

        # Check If User is Follower or not
        for follower in followers:
            if request.user == follower:
                is_follower = True
                break
            else:
                is_follower = False

        context = {
            'profile': profile,
            'user_posts': user_posts,
            'count_followers': followers_number,
            'is_follower': is_follower
        }

        return render(request, 'social/profile.html', context)


class EditUserProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'social/edit_profile.html'
    fields = ['name', 'bio', 'birthdate', 'country', 'avatar']

    def get_success_url(self):
        return reverse_lazy(
            'user_profile_page',
            kwargs={
                'pk': self.kwargs['pk']
            }
        )

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        user_profile = Profile.objects.filter(
            Q(user__username__icontains=query) |
            Q(name__icontains=query)
        )

        context = {
            'user_profile': user_profile
        }

        return render(request, 'social/search_results.html', context)