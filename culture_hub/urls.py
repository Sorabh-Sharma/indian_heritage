from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('directory/', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add/', views.add_item, name='add_item'),
    path('item/<str:pk>/', views.item_detail, name='item_detail'),
    path('item/<str:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<str:pk>/delete/', views.delete_item, name='delete_item'),
]
