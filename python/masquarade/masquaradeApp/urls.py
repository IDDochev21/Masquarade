from django.urls import path
from .views import login_view, register_view, landing_page

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', landing_page, name='landing'),
]