from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/messages/', include('messaging.urls')),  # This should now work without issue
    path('', views.home, name='home'),  # Root URL mapping
]
