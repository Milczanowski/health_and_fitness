from django.conf.urls import url

from accounts import views

urlpatterns = [
     url(r'^$', views.index ,name = 'ua_index'),
     url(r'add_meal/', views.add_meal ,name = 'add_meal'),
]