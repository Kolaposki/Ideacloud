"""
    name='urls',
    project='ideacloud'
    date='2/28/2020',
    author='Oshodi Kolapo',
"""
from django.urls import path
from . import views
from blog import views as blog_views
from django.contrib.auth import views as auth_views  # Use django inbuilt authentication to handle login and logout

urlpatterns = [
    path('', blog_views.home_page),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Resetiing password
    # a form to request for the password
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password-reset'),

    # view to infrom that the password has been resetted
    # Page displayed to the user after submitting the email form. Usually with instructions to open the email account,
    # look in the spam folder etc. And asking for the user to click on the link he will receive.
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password-reset-done'),

    # view to form for the new password
    # The link that was emailed to the user. This view will validate the token and display a password form if the token
    # is valid or an error message if the token is invalid (e.g. was already used or expired).
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password-reset-confirm'),

    path('password-reset_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password-reset-complete'),
]
