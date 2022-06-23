
from . import views
from django.urls import path 
from django.contrib.auth import views as auth_views 

# app_name = 'user'

urlpatterns = [
    path('login/', views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.registerUser,name='register'),
    
    path('',views.index_user, name='index_user'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='editAccount'),
    path('create-skill/',views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>', views.updateSkill,name='update-skill'),
    path('delete-skill/<str:pk>',views.deleteSkill,name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.messageView, name='message'),
    path('create-message/<str:pk>/', views.createMessage, name='create-message'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='user_app/reset_password.html'),
           name='reset_password'), 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user_app/reset_password_sent.html'), 
            name='password_reset_done'), 
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user_app/reset.html'),  
           name = 'password_reset_confirm'), 
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='user_app/reset_complete.html'), 
            name= 'password_reset_complete')

]