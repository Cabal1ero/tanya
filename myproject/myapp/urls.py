from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('add-review/', views.add_review, name='add_review'),
    path('services/', views.service_list, name='service_list'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    
    # API for booking form
    path('api/get-masters-for-service/<int:service_id>/', views.get_masters_for_service, name='get_masters_for_service'),
    path('api/get-time-slots/<int:master_id>/<str:date>/', views.get_time_slots, name='get_time_slots'),
    path('api/book-appointment/', views.book_appointment, name='book_appointment'),
]



