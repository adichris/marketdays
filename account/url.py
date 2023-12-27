from django.urls import path
from .views import LoginPage, LogOutRedirect


app_name = 'account'
urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    path("logout/", LogOutRedirect.as_view(), name="logout"),
]