from django.urls import path, re_path
from crud.views import CRUDView, GetUsersView, LoginView, LogoutView, SignupView

urlpatterns = [
    re_path('signup/', SignupView.as_view(), name='signup_view'),
    re_path('login/', LoginView.as_view(), name='login_view'),
    re_path('action/', CRUDView.as_view(), name='crud_view'),
    re_path('users/', GetUsersView.as_view(), name='users_view'),
    re_path('logout/', LogoutView.as_view(), name='logout_view')
]
