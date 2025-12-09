from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from newadmin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('accounts/', RedirectView.as_view(url='/', permanent=True)),
    path('newadmin/',include('newadmin.urls')),
    path('addlist/',views.addlist,name='addlist')
]