
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
]

from django.conf import settings
from django.conf.urls import include

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
