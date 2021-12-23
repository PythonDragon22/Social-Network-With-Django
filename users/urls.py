from django.urls import path
from users.views import registration_page, User_Signup_View, User_Signin_View, User_Signout_View, UserProfileView, EditUserProfile, UserSearchView


urlpatterns = [
	path('', registration_page, name="user_registration_page"),
    path('register/', User_Signup_View.as_view(), name="user_signup_page"),
    path('login/', User_Signin_View.as_view(), name="user_signin_page"),
    path('logout/', User_Signout_View.as_view(), name="user_signout_page"),
    path('search_results/', UserSearchView.as_view(), name="search_results"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="user_profile"),
	path('profile/edit/<int:pk>/', EditUserProfile.as_view(), name="edit_user_profile"),
]