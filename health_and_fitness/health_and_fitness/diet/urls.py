from django.conf.urls import url

from diet import views

urlpatterns = [
     url(r'^(?P<diet_id>[0-9]+)/', views.diet ,name = 'diet'),
     url(r'meal/add_com/', views.meal_add_com ,name = 'meal_add_com'),
     url(r'ingre/add_com/', views.ingre_add_com ,name = 'ingre_add_com'),
     url(r'add_com/', views.diet_add_com ,name = 'diet_add_com'),
     url(r'meal/(?P<meal_id>[0-9]+)/', views.meal ,name = 'meal'),
     url(r'meals/', views.meals ,name = 'meals'),
     url(r'ingres/', views.ingres ,name = 'ingres'),
     url(r'ingre/(?P<ingre_id>[0-9]+)/', views.ingre ,name = 'ingre'),

]