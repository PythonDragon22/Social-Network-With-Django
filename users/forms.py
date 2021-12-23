from django import forms
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth import authenticate


class User_Signup_Form(forms.Form):
    username= forms.CharField(label= '', widget=forms.TextInput(attrs={"class": "input-field", 'placeholder': 'John Doe'}))
    email= forms.EmailField(label= '', widget=forms.EmailInput(attrs={"class": "input-field", 'placeholder': 'johndoe@gmail.com'}))
    first_name= forms.CharField(label= '', widget=forms.TextInput(attrs={"class": "input-field", 'placeholder': 'John'}))
    last_name= forms.CharField(label= '', widget=forms.TextInput(attrs={"class": "input-field", 'placeholder': 'Doe'}))
    password= forms.CharField(label= '', widget=forms.PasswordInput(attrs={ "class": "input-field", 'placeholder': 'Password'}))
    password_confirmation= forms.CharField(label= '', widget=forms.PasswordInput(attrs={ "class": "input-field", 'placeholder': 'Password Confirmation'}))


class User_Signin_Form(forms.Form):
    username= forms.CharField(label= '', widget=forms.TextInput(attrs={"class": "input-field", 'placeholder': 'John Doe'}))
    password= forms.CharField(label= '', widget=forms.PasswordInput(attrs={ "class": "input-field", 'placeholder': 'Password'}))

    error_messages = {
        'invalid_login': "Please enter a correct username and password."
                           "Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }


    def confirm_login_allowed(self, user):          ## Control whether the given User may log in.
        if not user.is_active:     ## If user.is_active == False ... raise ValidationError.
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def clean(self):         ## Form Fields Validation.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user)
        return self.cleaned_data


    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__exact=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['username', 'email', 'first_name', 'last_name']
        widgets= {
        'username': forms.TextInput(attrs= {'class' : 'input-field'}),
        'email': forms.EmailInput(attrs= {'class' : 'input-field'}),
        'first_name': forms.TextInput(attrs= {'class' : 'first_name'}),
        'last_name': forms.TextInput(attrs= {'class' : 'last_name'}),
        }


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label= '')
    class Meta:
        model= Profile
        fields= ['bio', 'birthdate', 'country', 'avatar']
        # exclude= ['user', 'created_at', 'updated_at']

        widgets= {
        'bio': forms.Textarea(attrs= {'class' : 'bio'}),
        'birthdate': forms.SelectDateWidget(attrs= {'class' : 'date'}),
        'country': forms.TextInput(attrs= {'class' : 'input-field'}),
        }