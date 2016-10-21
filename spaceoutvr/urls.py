from django.conf.urls import url
from spaceoutvr import views

urlpatterns = [
        url(r'^home/', views.home),
        ]
