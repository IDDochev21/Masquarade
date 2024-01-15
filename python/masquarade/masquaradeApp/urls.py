from django.urls import path
from .views import login_view, register_view, landing_page, home_view, digital_will_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', landing_page, name='landing'),
    path('digital_will/', digital_will_view, name='digital_will'),
]
