from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/',views.user_logout,name='logout'),
    path('update/<int:pk>/', views.update_review, name='update_review'),
    path('reporting/', views.reporting, name='reporting'),
    path('api/generate-notification/', views.generate_notification, name='generate_notification'),
    path('add_reviewer/',views.add_reviewer,name='add_reviewer'),
    path('remarks/<int:review_id>/',views.remarks,name='remarks'),
    path('feedback/<int:review_id>/',views.feedback,name='feedback'),
]