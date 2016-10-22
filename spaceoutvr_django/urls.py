from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^', include('spaceoutvr.urls')),
    url('', include('user_management.api.urls', namespace='user_management_api')),
)
