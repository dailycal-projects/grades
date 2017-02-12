from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from graphic.views import GraphicView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grades/$', GraphicView.as_view()),
]