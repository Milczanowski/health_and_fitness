from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class IngredientType(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name

class Ingredient(models.Model):
    Image           = models.ImageField(upload_to='ingre_image/', default ='ingre_image/default.jpg')
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name

class Unit(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)

    def __unicode__(self):
        return self.Name

class FoodIngredient(models.Model):
    Ingredient      = models.ForeignKey(Ingredient, null = False, blank = False)
    Number          = models.FloatField(default = 0.0)
    Unit            = models.ForeignKey(Unit, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)

    def __unicode__(self):
        return '%s %s of %s' % (self.Number, self.Unit, self.Ingredient)


class Meal(models.Model):
    Image           = models.ImageField(upload_to='meals_image/', default ='meals_image/default.jpg')
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)
    Ingredients     = models.ManyToManyField(FoodIngredient)
    Types           = models.ManyToManyField(IngredientType)
    Time            = models.TimeField(default= datetime.time(00,00)) 
    Rating          = models.IntegerField(default = 0)
    Rating_Count    = models.IntegerField(default = 0)

    def get_rating(self):
        if self.Rating_Count == 0:
            return 0
        return self.Rating/ self/Rating_Count

    def get_time(self):
        return self.Time.strftime('%H:%M:%S')

    def __unicode__(self):
        return self.Name

class MealComment(models.Model):
    Content         = models.TextField(default= "", null = False, blank =False)
    Author          = models.ForeignKey(User, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Meal            = models.ForeignKey(Meal, null = False, blank = False)


class DietType(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name


class Diet(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Meals           = models.ManyToManyField(Meal)
    Types           = models.ManyToManyField(DietType)
    Description     = models.TextField(default= "", null = True, blank = True)
    Rating          = models.IntegerField(default = 0)
    Rating_Count    = models.IntegerField(default = 0)

    def get_rating(self):
        if self.Rating_Count == 0:
            return 0
        return self.Rating/ self/Rating_Count
        


    def __unicode__(self):
        return self.Name


class DietComment(models.Model):
    Content         = models.TextField(default= "", null = False, blank =False)
    Author          = models.ForeignKey(User, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Diet            = models.ForeignKey(Diet, null = False, blank = False)

    