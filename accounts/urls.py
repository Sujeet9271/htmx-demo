from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views

    
    # user accounts routes
app_name = "accounts"

urlpatterns = [
    path('',index,name="index"),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'), 
    path('login/',auth_login,name='login'),

    path('events/',get_all_events,name="get_all_events"),
    path('events/create/',create_event,name='create_event'),
    path('events/<int:id>/edit',edit_event,name='edit_event'),
    path('events/<int:id>/delete',delete_event,name='delete_event'),
    
    path('scroll/',get_all_users,name="get_all_users"),
    
    path('tickets/',tickets,name="tickets"),
    path('ticket_list/',get_all_tickets,name="get_all_tickets"),


    path('logout/',log_out,name="logout"),
    
]