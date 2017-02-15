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
    Types           = models.ManyToManyField(IngredientType)

    def __unicode__(self):
        return self.Name


class IngredientComment(models.Model):
    Content         = models.TextField(default= "", null = False, blank =False)
    Author          = models.ForeignKey(User, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Ingredient            = models.ForeignKey(Ingredient, null = False, blank = False)

    def reference(self):
        return self.Ingredient

    def get_admin_url(self):
        return '/admin/diet/ingredientcomment/%s/' % self.id


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

class MealType(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name


class Meal(models.Model):
    Image           = models.ImageField(upload_to='meals_image/', default ='meals_image/default.jpg')
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)
    Ingredients     = models.ManyToManyField(FoodIngredient)
    Types           = models.ManyToManyField(MealType)
    Time            = models.IntegerField(default = 0) 
    Rating          = models.IntegerField(default = 0)
    Rating_Count    = models.IntegerField(default = 0)
    Difficulty      = models.IntegerField(default = 0)
    c_ratting        = models.FloatField(default = 0)
    Voters          = models.ManyToManyField(User, blank = True, related_name='voters_meal')


    def get_rating(self):
        if self.Rating_Count == 0:
            return 0
        return self.Rating/ float(self.Rating_Count)

    def get_time(self):
        return '%s m' % self.Time

    def __unicode__(self):
        return self.Name

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        self.c_ratting = self.get_rating()
        return super(Meal, self).save(force_insert, force_update, using, update_fields)

    def rating_enable(self, user):
        return not self.Voters.filter(id = user.id).exists()

    def add_rating(self, user, rating):
        self.Rating+= rating
        self.Rating_Count+=1
        self.Voters.add(user)
        self.save()

class MealComment(models.Model):
    Content         = models.TextField(default= "", null = False, blank =False)
    Author          = models.ForeignKey(User, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Meal            = models.ForeignKey(Meal, null = False, blank = False)

    def reference(self):
        return self.Meal

    def get_admin_url(self):
        return '/admin/diet/mealcomment/%s/' % self.id


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
    Voters          = models.ManyToManyField(User, blank = True, related_name='voters_diet')

    def get_rating(self):
        if self.Rating_Count == 0:
            return 0
        return self.Rating/ float(self.Rating_Count)

    def __unicode__(self):
        return self.Name

    def rating_enable(self, user):
        return not self.Voters.filter(id = user.id).exists()

    def add_rating(self, user, rating):
        self.Rating+= rating
        self.Rating_Count+=1
        self.Voters.add(user)
        self.save()


class DietComment(models.Model):
    Content         = models.TextField(default= "", null = False, blank =False)
    Author          = models.ForeignKey(User, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Diet            = models.ForeignKey(Diet, null = False, blank = False)

    def reference(self):
        return self.Diet

    def get_admin_url(self):
        return '/admin/diet/dietcomment/%s/' % self.id