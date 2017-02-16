from datetime import datetime
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from diet import views
from django.views.static import serve


urlpatterns = [
     url(r'^forum/',  include('forum.urls')),
     url(r'^user/',  include('accounts.urls')),
     url(r'^diet/',  include('diet.urls')),
     url(r'^admin/', include(admin.site.urls)),

     url(r'^register/$', views.register ,name = 'register'),
     url(r'^login/$', views.login ,name = 'login'),
     url(r'^logout/$', views.logout ,name = 'logout'),
     url(r'^$', views.index ,name = 'index'),
     url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]
