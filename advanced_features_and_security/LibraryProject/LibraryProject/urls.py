
from django.contrib import admin
from django.urls import path
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns = [
    path('relationship/', include('relationship_app.urls')),
]
