from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path("assign/<int:ticket_id>/", views.assign_ticket, name="assign_ticket"),
    path("update/<int:ticket_id>/", views.update_status, name="update_status"),
    path("ticket/<int:ticket_id>/", views.ticket_details, name="ticket_details"),
    path("attachment/delete/<int:attachment_id>/", views.delete_attachment, name="delete_attachment"),
    path("reports/", views.reports, name="reports"),
]    