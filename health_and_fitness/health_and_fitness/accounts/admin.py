from django.contrib import admin
from accounts.models import UserAccount

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('User', 'favorite_diets_count', 'favorite_meals_count', 'Creation_Data')

    def favorite_diets_count(self,obj):
        return obj.Favorite_Diets.count()

    def favorite_meals_count(self,obj):
        return obj.Favorite_Meals.count()

admin.site.register(UserAccount, UserAccountAdmin)
