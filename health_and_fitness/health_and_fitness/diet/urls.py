from django.conf.urls import url

from diet import views

urlpatterns = [
     url(r'^(?P<diet_id>[0-9]+)/', views.diet ,name = 'diet'),
     url(r'add_com/', views.diet_add_com ,name = 'diet_add_com'),
     url(r'meal/(?P<meal_id>[0-9]+)/', views.meal ,name = 'meal'),
     url(r'meals/', views.meals ,name = 'meals'),
     url(r'meal/add_com/', views.meal_add_com ,name = 'meal_add_com'),
     url(r'ingres/', views.ingres ,name = 'ingres'),
]