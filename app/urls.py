from django.urls import path
from .views import AllRegistrationAPIView
urlpatterns=[
   path('all-registration/',AllRegistrationAPIView.as_view(),name='all-registration'),
]