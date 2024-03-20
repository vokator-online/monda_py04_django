from django.urls import path
from . import views

urlpatterns = [
     path('new/', views.TicketCreateView.as_view(), name='ticket_create'),
]
