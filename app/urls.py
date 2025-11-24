from django.urls import path
from .views import AllRegistrationAPIView, ChangePasswordAPIView, CreateProfileAPIView, LoginAPIView, RefreshTokenAPIView, UserDetailAPIView
urlpatterns=[
   path('all-registration/',AllRegistrationAPIView.as_view(),name='all-registration'),
   path('login/',LoginAPIView.as_view(),name='login'),
   path('user-detail/',UserDetailAPIView.as_view(),name='user-detail'),
   path("token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
   path("change-password/",ChangePasswordAPIView.as_view(),name="change_password"),
   path("create-profile/",CreateProfileAPIView.as_view(),name='create-profile')
]