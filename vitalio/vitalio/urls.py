# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super/', admin.site.urls),
    path('', include('pages.urls')),
    path('_/', include('account.urls')),
    # path('company/', include('company.urls')),
    path('member/', include('member.urls')),
    path('onboard/', include('onboard.urls')),
    path('provider/', include('provider.urls')),
    path('room/', include('room.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)