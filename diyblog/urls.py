from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include blog URLs at root
    path('accounts/', include('django.contrib.auth.urls')),
]