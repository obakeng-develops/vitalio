# Django
from django.contrib import admin
from django.urls import path, include

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
