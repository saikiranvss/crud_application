from django.urls import path, re_path
from crud.views import CRUDView, LoginView, SignupView

urlpatterns = [
    re_path('signup/', SignupView.as_view(), name='signup_view'),
    re_path('login/', LoginView.as_view(), name='login_view'),
    re_path('action/', CRUDView.as_view(), name='crud_view')
]
