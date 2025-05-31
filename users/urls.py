from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import loginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

