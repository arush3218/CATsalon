from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),
    path('logout/', views.logoutUser, name = 'logout'), 
    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('create-room/', views.createRoom, name = 'create_room'),
    path('update-room/<str:pk>', views.updateRoom, name = 'update_room'),
    path('delete-room/<str:pk>', views.DeleteRoom, name = 'delete_room'),
    path('delete-message/<str:pk>', views.DeleteMessage, name = 'delete_message'),
    
]
