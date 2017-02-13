from django.contrib import admin
from diet.models import Ingredient, Dish, IngredientType,FoodIngredient, Unit, Diets, DietType
from django.db.models import Sum

class UnitAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'dish_count', 'Creation_Data')

    def dish_count(self, obj):
        return Dish.objects.filter(Ingredients__Ingredient = obj).distinct().count()

class DishAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'ingredient_count', 'types_count', 'Creation_Data')

    def ingredient_count(self, obj):
        return obj.Ingredients.count()

    def types_count(self, obj):
        return obj.Types.count()

class FoodIngredientAdmin(admin.ModelAdmin):
    list_display = ('Ingredient', 'Number', 'Unit', 'dish_count', 'Creation_Data')

    def dish_count(self, obj):
        return obj.dish_set.count()

class DietTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class DietsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'dishs_count', 'types_count', 'Creation_Data')


    def dishs_count(self, obj):
        return obj.Dishs.count()

    def types_count(self, obj):
        return obj.Types.count()


admin.site.register(Unit, UnitAdmin)
admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish,DishAdmin)
admin.site.register(FoodIngredient, FoodIngredientAdmin)
admin.site.register(DietType, DietTypeAdmin)
admin.site.register(Diets, DietsAdmin)