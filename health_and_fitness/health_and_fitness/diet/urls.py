from django.conf.urls import url

from diet import views

urlpatterns = [
     url(r'^(?P<diet_id>[0-9]+)/', views.diet ,name = 'diet'),
     url(r'meal/rate/', views.rate_meal,name = 'rate_meal'),   
     url(r'rate/', views.rate_diet ,name = 'rate_diet'),     
     url(r'meal/add_com/', views.meal_add_com ,name = 'meal_add_com'),
     url(r'ingre/add_com/', views.ingre_add_com ,name = 'ingre_add_com'),
     url(r'add_com/', views.diet_add_com ,name = 'diet_add_com'),
     url(r'meal/(?P<meal_id>[0-9]+)/', views.meal ,name = 'meal'),
     url(r'meals/', views.meals ,name = 'meals'),
     url(r'ingres/', views.ingres ,name = 'ingres'),
     url(r'ingre/(?P<ingre_id>[0-9]+)/', views.ingre ,name = 'ingre'),

     url(r'add_unit/', views.add_unit ,name = 'add_unit'),
     url(r'add_ingre_type/', views.add_ingre_type, name = 'add_ingre_type'),
     url(r'add_ingre/', views.add_ingre, name = 'add_ingre'),
     url(r'add_meal_type/', views.add_meal_type, name = 'add_meal_type'),
     url(r'add_recipe/', views.add_recipe ,name = 'add_recipe'),
]