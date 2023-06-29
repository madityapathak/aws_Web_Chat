from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
   
    path('login/', views.log_in ,name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('recovery/', views.account_search_page, name='passwordreset'),
    path('',views.home,name='home'),
    path('logout/', views.log_out ,name='logout'),
    path('activation-email-validation/<uidb64>/<token>/', views.activation_email_validator ,name='activate'),
    path('recover/<str:pk>/', views.send_password_reset_email, name='psresetter'),
    path('update-password/<uidb64>/<unameb64>/', views.update_password, name='reset-password'),
    path('password-email-validation/<uidb64>/<token>/<unameb64>/', views.password_email_validator ,name='password-reset'),
    path('edit/<str:pk>/',views.edit_account,name='edit-account'),
    path('<user_id>/edit/cropImage/', views.crop_image, name="crop_image"),
    path('remove/profileImage/', views.remove_profile_image, name="remove-profile-image"),
    path('about/',views.about_page,name="about-page"),
]