from django.db import models
from django.contrib.auth.models import User
from diet.models import Diet, Meal
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils import timezone

class UserAccount(models.Model):
    User             = models.OneToOneField(User,primary_key=True)
    Favorite_Diets   = models.ManyToManyField(Diet, blank = True)
    Favorite_Meals   = models.ManyToManyField(Meal, blank = True)
    Creation_Data   = models.DateTimeField(default = timezone.now)


    def is_favorite_meal(self, meal):
        return self.Favorite_Meals.filter(id = meal.id).exists()

    def is_favorite_diet(self, diet):
        return self.Favorite_Diets.filter(id = diet.id).exists()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userAccount, _ = UserAccount.objects.get_or_create(User= instance)
        if _:
            userAccount.save()

        cacheUserAccount.add(userAccount)

post_save.connect(create_user_profile, sender=User)  
