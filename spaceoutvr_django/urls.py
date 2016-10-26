from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^', include('spaceoutvr.urls')),
    # url(r'^api/accounts/', include('spaceoutvr.urls')),
    # url(r'^', include('authemail.urls')),
    url(r'^api/accounts/', include('authemail.urls')),
    # url(r'^api/accounts/', include('rest_framework.urls', namespace='rest_framework'))
)
