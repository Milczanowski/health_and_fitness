from django.conf.urls import url

from forum import views

urlpatterns = [
     url(r'add_new_topic/', views.add_new_topic ,name = 'add_new_topic'),
     url(r'add_new_post/', views.add_new_post ,name = 'add_new_post'),
     url(r'^(?P<topic_id>[0-9]+)/', views.topic ,name = 'topic'),
     url(r'^$', views.index ,name = 'index'),

]