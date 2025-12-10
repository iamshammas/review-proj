from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='reg'),
    path('advisors/',views.advisor_list,name='advisors'),
    path('review_count/',views.review_count,name='review_count'),
]