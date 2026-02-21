from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('agent/', views.agent_dummy_view, name='agent_dummy'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
    path('laws/', views.farmer_laws_view, name='farmer_laws'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
