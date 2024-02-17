from django.urls import path    
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    # path('change-password/', PasswordChange.as_view(), name='changepass'),
    path('logout/', UserLogout.as_view(), name='logout'),
]