from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_settings/', UserEditView.as_view(), name='edit-settings'),
    path('password/', PasswordsChangeView.as_view(
        template_name='registration/change-password.html')),
    path('password_success', views.password_success, name='password_success'),
    path('<int:pk>/edit_profile_page/',
         EditProfilePageView.as_view(), name='edit_profile_page'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='profile'),
    path('create_profile_page/', CreateProfilePageView.as_view(),
         name='create_profile_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
