from django.contrib import admin
from diet.models import Ingredient, Meal, IngredientType,FoodIngredient, Unit, Diet, DietType, MealType, IngredientComment, MealComment, DietComment
from django.db.models import Sum
from django.template import loader

class UnitAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'meal_count', 'Creation_Data','image')
    readonly_fields = ('comments',)
    extra_field = ('comments',)

    def meal_count(self, obj):
        return Meal.objects.filter(Ingredients__Ingredient = obj).distinct().count()

    def image(self, obj):
        return '<img src="/media/%s" alt="%s" style="width:50px;height:50px;">' % (obj.Image, obj.Name)
    image.allow_tags = True

    def comments(self, obj):
        return loader.get_template('comment_list_admin.html').render({'comments': obj.ingredientcomment_set.all()})
    comments.allow_tags = True

class MealAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'ingredient_count', 'types_count', 'Time', 'rating', 'Difficulty', 'Creation_Data', 'image')
    readonly_fields = ('comments',)
    extra_field = ('comments',)

    def ingredient_count(self, obj):
        return obj.Ingredients.count()

    def types_count(self, obj):
        return obj.Types.count()

    def rating(self, obj):
        return obj.get_rating()

    def image(self, obj):
        return '<img src="/media/%s" alt="%s" style="width:50px;height:50px;">' % (obj.Image, obj.Name)
    image.allow_tags = True

    def comments(self, obj):
        return loader.get_template('comment_list_admin.html').render({'comments': obj.mealcomment_set.all()})
    comments.allow_tags = True

class FoodIngredientAdmin(admin.ModelAdmin):
    list_display = ('Ingredient', 'Number', 'Unit', 'meal_count', 'Creation_Data')

    def meal_count(self, obj):
        return obj.meal_set.count()

class DietTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data')

class DietsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'meals_count', 'types_count', 'Creation_Data')
    readonly_fields = ('comments',)
    extra_field = ('comments',)


    def meals_count(self, obj):
        return obj.Meals.count()

    def types_count(self, obj):
        return obj.Types.count()

    def comments(self, obj):
        return loader.get_template('comment_list_admin.html').render({'comments': obj.dietcomment_set.all()})
    comments.allow_tags = True

class CommentAdmin(admin.ModelAdmin):
    list_display = ('Author', 'Content', 'Creation_Data', 'reference')


admin.site.register(Unit, UnitAdmin)
admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal,MealAdmin)
admin.site.register(FoodIngredient, FoodIngredientAdmin)
admin.site.register(DietType, DietTypeAdmin)
admin.site.register(Diet, DietsAdmin)
admin.site.register(MealType,IngredientTypeAdmin)
admin.site.register(IngredientComment, CommentAdmin)
admin.site.register(MealComment, CommentAdmin)
admin.site.register(DietComment, CommentAdmin)