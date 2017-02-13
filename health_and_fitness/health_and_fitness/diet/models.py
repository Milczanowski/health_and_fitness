from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class IngredientType(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name

class Ingredient(models.Model):
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


class Dish(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)
    Ingredients     = models.ManyToManyField(FoodIngredient)
    Types           = models.ManyToManyField(IngredientType)

    def __unicode__(self):
        return self.Name

class DietType(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name


class Diets(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Dishs           = models.ManyToManyField(Dish)
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
    