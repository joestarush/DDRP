from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name = 'dashboard'),
    path('user/signup', views.user_signup, name = 'user_signup'),
    path('victim/signup', views.victim_signup, name = 'victim_signup'),
    path('admin/otp', views.admin_otp, name = 'admin_otp'),
    path('admin/signup', views.admin_signup, name = 'admin_signup'),
    path('signin', views.signin, name = 'signin'),
    path('forgot_password', views.forgot_password, name = 'forgot_password'),
    path('signout', views.signout, name = 'signout'),
    path('user/signup', views.user_signup, name = 'user_signup'),
    path('victim/signup', views.victim_signup, name = 'victim_signup'),
    path('victim/otp', views.victim_otp, name = 'victim_otp'),
    path('user/otp', views.user_otp, name = 'user_otp'),
    path('admin/generate', views.generate_requirements_admin, name = 'generate_requirements_admin'),
    path('view_requirements', views.view_requirements, name = 'view_requirements'),
    path('track', views.track_requirements, name = 'track_requirements'),
    path('log', views.log_requirements, name = 'log_requirements'),
    path('donate_now', views.donate_now, name = 'donate_now'),
    path('currloc', views.currloc, name = 'currloc'),
    path('victim/generate', views.victim_generate, name = 'victim_generate'),
    path('approve_now', views.approve_now, name = 'approve_now'),
    path('victim/track', views.track_requirements_victim, name = 'track_requirements_victim'),
    path('log_camera', views.log_camera, name = 'log_camera'),
    path('fill_data', views.fill_data, name = 'fill_data'),
    path('send', views.send, name = 'send')
]