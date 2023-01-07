from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('create/',views.create,name="create"),
    path('vote/<int:pk>',views.vote,name='vote'),
    path('result/<int:pk>',views.result,name = "result"),
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.view_profile,name='profile'),
]