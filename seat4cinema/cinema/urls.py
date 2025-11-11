from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('book/<int:showtime_id>/', views.book_ticket, name='book_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('cancel-booking/<int:ticket_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
]