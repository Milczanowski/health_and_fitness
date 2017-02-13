from django.contrib import admin
from diet.models import Ingredient, Meal, IngredientType,FoodIngredient, Unit, Diets, DietType
from django.db.models import Sum

class UnitAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'meal_count', 'Creation_Data')

    def meal_count(self, obj):
        return Meal.objects.filter(Ingredients__Ingredient = obj).distinct().count()

class MealAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'ingredient_count', 'types_count','Time', 'Creation_Data', 'image')

    def ingredient_count(self, obj):
        return obj.Ingredients.count()

    def types_count(self, obj):
        return obj.Types.count()

    def image(self, obj):
        return '<img src="/media/%s" alt="%s" style="width:50px;height:50px;">' % (obj.Image, obj.Name)


    image.allow_tags = True


class FoodIngredientAdmin(admin.ModelAdmin):
    list_display = ('Ingredient', 'Number', 'Unit', 'meal_count', 'Creation_Data')

    def meal_count(self, obj):
        return obj.meal_set.count()

class DietTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class DietsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'meals_count', 'types_count', 'Creation_Data')


    def meals_count(self, obj):
        return obj.Meals.count()

    def types_count(self, obj):
        return obj.Types.count()


admin.site.register(Unit, UnitAdmin)
admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal,MealAdmin)
admin.site.register(FoodIngredient, FoodIngredientAdmin)
admin.site.register(DietType, DietTypeAdmin)
admin.site.register(Diets, DietsAdmin)