from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from ntroje_backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/', include('accounts.urls')),

    # Agency
    path('api/agency/', include('agency.urls')),
    # Properties
    path('api/properties/', include('properties.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
