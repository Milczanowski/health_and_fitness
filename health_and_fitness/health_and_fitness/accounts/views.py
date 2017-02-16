from django.shortcuts import render, redirect
from diet.models import Diet, Meal, IngredientType, MealType, Ingredient, Unit

def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')


    return render(request, 'index.html', {'content': render(request, 'user_account.html', {
             'user_account': request.user.useraccount,
             'meals': Meal.objects.filter(Creator = request.user)
             }).content}, content_type='application/xhtml+xml')


def add_meal(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    return render(request, 'index.html', {'content': render(request, 'add_meal.html', {
                'ing_type': IngredientType.objects.all(),
                'recipe_type': MealType.objects.all(),
                'recipe_ingre': Ingredient.objects.all(),
                'units':Unit.objects.all(),
                }).content}, content_type='application/xhtml+xml')