from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from fruit_shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('goods.urls')),
    path('auth/', include('users.urls')),
]
