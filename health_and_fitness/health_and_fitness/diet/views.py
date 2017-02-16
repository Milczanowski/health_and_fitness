from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError,  ObjectDoesNotExist
from django.contrib.auth import logout as _logout, authenticate, login as _login
from diet.models import Diet, Meal, MealComment, DietComment, Ingredient, IngredientComment,  MealType, Unit, IngredientType, MealType, FoodIngredient
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
import json

diets_count = 20
meals_count = 20
ingres_count = 20

def is_email_correct(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def index(request):
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']

    diets_all = Diet.objects.all()
    diets = Paginator(diets_all, diets_count)

    try:
        diets = diets.page(page)
    except EmptyPage as e:
        diets = diets.page(1)
        page = 1

    pages = []
        
    if diets.has_previous():
        pages.append(diets.previous_page_number())

    if diets.has_other_pages():
        pages.append(page)

    if diets.has_next():
        pages.append(diets.next_page_number())


    return render(request, 'index.html', {'content': render(request, 'diets.html', { 'diets': diets, 'pages': pages, 'current_page': page}).content}, content_type='application/xhtml+xml')

def register(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'content': render(request, 'register.html').content}, content_type='application/xhtml+xml')
    else:
        username = request.POST['username']
        password = request.POST['password']
        email    = request.POST['email']

        errors = []

        if User.objects.filter(username = username).exists():
            errors.append('USER ALREADY EXISTS.')

        if User.objects.filter(email = email).exists():
            errors.append('EMAIL ALREADY EXISTS.')

        if len(password) < 6:
            errors.append('PASSWORD IS TOO SHORT.')

        if not is_email_correct(email):
            errors.append('INVALID EMAIL.')

        if len(errors)!= 0:
            return render(request, 'index.html', {'content': render(request, 'register.html', {'errors': errors}).content}, content_type='application/xhtml+xml')
        else:
            user = User.objects.create_user(username,email,password)
            user.save()
            return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'content': render(request, 'login.html').content}, content_type='application/xhtml+xml')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username = username)
        if not user.exists():
            return render(request, 'index.html', {'content': render(request, 'login.html',{'errors': ['USER NOT EXISTS.']}).content}, content_type='application/xhtml+xml')

        user = authenticate(username= username, password= password)
        if user is None:
            return render(request, 'index.html', {'content': render(request, 'login.html',{'errors': ['INCORRECT PASSWORD.']}).content}, content_type='application/xhtml+xml')

        _login(request, user)
        return redirect('/')

def logout(request):
    if request.user.is_authenticated():
        _logout(request)
    return redirect('/')

def diet(request, diet_id):
    try:
        diet = Diet.objects.get(id = diet_id)

        if request.method == 'POST':
            if 'remove_from_f' in request.POST:
                request.user.useraccount.Favorite_Diets.remove(diet)

            if 'add_to_f' in request.POST:
                request.user.useraccount.Favorite_Diets.add(diet)


        return render(request, 'index.html', {'content': render(request, 'diet.html', { 'diet': diet, 'rating_enable': diet.rating_enable(request.user), 'is_favorite': request.user.useraccount.is_favorite_diet(diet) }).content}, content_type='application/xhtml+xml')
    except ObjectDoesNotExist as e:
        return redirect('/')

class Search_Param():
    
    def __init__(self):
        self.search_param = dict()

    def clear(self, session):
        self.search_param[session] = dict()

    def add(self, session, post_param):
        self.search_param[session] = dict()

        if 'type' in post_param:
            self.search_param[session]['type'] = post_param['type']

        if 'max_time' in post_param:
            self.search_param[session]['max_time'] = post_param['max_time']

        if 'max_diff' in post_param:
            self.search_param[session]['max_diff'] = post_param['max_diff']

        if 'min_rat' in post_param:
            self.search_param[session]['min_rat'] = post_param['min_rat']

        if 'ingre' in post_param:
            self.search_param[session]['ingre'] = post_param['ingre']

    def get_meals(self, session):
        meals = Meal.objects.all()

        if session in self.search_param:
            if  'max_time' in  self.search_param[session]:
                if int(self.search_param[session]['max_time'])!= 0:
                    meals = meals.filter(Time__lte =int(self.search_param[session]['max_time']))

            if  'max_diff' in  self.search_param[session]:
                if int(self.search_param[session]['max_diff'])!= 0:
                    meals = meals.filter(Difficulty__lte =int(self.search_param[session]['max_diff']))

            if  'min_rat' in  self.search_param[session]:
                if int(self.search_param[session]['min_rat'])!= 0:
                    meals = meals.filter(c_ratting__gte =int(self.search_param[session]['min_rat']))

            if  'type' in  self.search_param[session]:
                meals = meals.filter(Types__in= self.search_param[session]['type'])

            if  'ingre' in  self.search_param[session]:
                meals = meals.filter(Ingredients__Ingredient__in = self.search_param[session]['ingre'])

        return meals


search_param = Search_Param()

def meals(request):
    page = 1

    if request.method == 'GET':
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            search_param.clear(request.session)
    else:
        search_param.add(request.user.id, request.POST)

    meals_all = search_param.get_meals(request.user.id)
    meals = Paginator(meals_all, 20)

    try:
        meals = meals.page(page)
    except EmptyPage as e:
        meals = meals.page(1)
        page = 1

    pages = []
        
    if meals.has_previous():
        pages.append(meals.previous_page_number())

    if meals.has_other_pages():
        pages.append(page)

    if meals.has_next():
        pages.append(meals.next_page_number())

    typess = []       
    typess.append([])
    index = 0
    for type in MealType.objects.all():
        typess[index].append(type)
        if(len(typess[index])>=10):
            index+=1
            typess.append([])

    ingress = []
    ingress.append([])
    index = 0
    for ingre in Ingredient.objects.all():
        ingress[index].append(ingre)
        if(len(ingress[index])>=10):
            index+=1
            ingress.append([])


    return render(request, 'index.html', {'content': render(request, 'meals.html', { 'meals': meals, 'pages': pages, 'current_page': page, 'typess': typess, 'ingress': ingress }).content}, content_type='application/xhtml+xml')


def meal(request, meal_id):
    try:
        meal = Meal.objects.get(id = meal_id)

        if request.method == 'POST':
            if 'remove_from_f' in request.POST:
                request.user.useraccount.Favorite_Meals.remove(meal)

            if 'add_to_f' in request.POST:
                request.user.useraccount.Favorite_Meals.add(meal)


        return render(request, 'index.html', {'content': render(request, 'meal.html', { 'meal': meal,  'rating_enable': meal.rating_enable(request.user), 'is_favorite': request.user.useraccount.is_favorite_meal(meal) }).content}, content_type='application/xhtml+xml')
    except ObjectDoesNotExist as e:
        return redirect('/diet/meals/')
    
 
def meal_add_com(request):
    if request.method != 'POST':
        return redirect('/diet/meals/')

    if not request.user.is_authenticated():
        return redirect('/login/')

    meal_com = MealComment(Author = request.user, Content = request.POST['content'], Meal_id = request.POST['id'])
    meal_com.save()
    return redirect('/diet/meal/%s/' % request.POST['id'])


def diet_add_com(request):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated():
        return redirect('/login/')

    diet_com = DietComment(Author = request.user, Content = request.POST['content'], Diet_id = request.POST['id'])
    diet_com.save()
    return redirect('/diet/%s/' % request.POST['id'])    


def ingres(request):
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']

    ingres_all = Ingredient.objects.all()
    ingres = Paginator(ingres_all, ingres_count)

    try:
        ingres = ingres.page(page)
    except EmptyPage as e:
        ingres = ingres.page(1)
        page = 1

    pages = []
        
    if ingres.has_previous():
        pages.append(ingres.previous_page_number())

    if ingres.has_other_pages():
        pages.append(page)

    if ingres.has_next():
        pages.append(ingres.next_page_number())


    return render(request, 'index.html', {'content': render(request, 'ingres.html', { 'ingres': ingres, 'pages': pages, 'current_page': page}).content}, content_type='application/xhtml+xml')

def ingre(request, ingre_id):
    try:
        ingre = Ingredient.objects.get(id = ingre_id)

        return render(request, 'index.html', {'content': render(request, 'ingre.html', { 'ingre': ingre }).content}, content_type='application/xhtml+xml')
    except ObjectDoesNotExist as e:
        return redirect('/diet/ingres/')

def ingre_add_com(request):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated():
        return redirect('/login/')

    ingre_com = IngredientComment(Author = request.user, Content = request.POST['content'], Ingredient_id = request.POST['id'])
    ingre_com.save()
    return redirect('/diet/ingre/%s/' % request.POST['id'])    

def rate_diet(request):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated():
        return redirect('/login/')
    try:
        diet = Diet.objects.get(id = request.POST['id'])
        diet.add_rating(request.user, int(request.POST['rate']))

        return redirect('/diet/%s/' % request.POST['id'])
    except ObjectDoesNotExist as e:
        return redirect('/')

def rate_meal(request):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated():
        return redirect('/login/')
    try:
        meal = Meal.objects.get(id = request.POST['id'])
        meal.add_rating(request.user, int(request.POST['rate']))

        return redirect('/diet/meal/%s/' % request.POST['id'])
    except ObjectDoesNotExist as e:
        return redirect('/')


def add_unit(request):
    if request.method != 'POST':
        return HttpResponse('[]')

    if not request.user.is_authenticated():
        return HttpResponse('[]')

    if 'unit' not in request.POST:
        return HttpResponse('[]')

    if len(request.POST['unit'])!=0:
        try:
            unit, _ = Unit.objects.get_or_create( Name = request.POST['unit'], Creator = request.user)
            unit.save()

            if _:
                return HttpResponse('[%s]' % unit.get_json())
        except IntegrityError:
            pass

    return HttpResponse('[]')

def add_ingre_type(request):
    if request.method != 'POST':
        return HttpResponse('[]')

    if not request.user.is_authenticated():
        return HttpResponse('[]')

    if 'name' not in request.POST or 'desc' not in request.POST:
        return HttpResponse('[]')

    if len(request.POST['name'])!=0:
        try:
            i_t, _ = IngredientType.objects.get_or_create( Name = request.POST['name'], Creator = request.user, Description = request.POST['desc'])
            i_t.save()
            if _:
                return HttpResponse('[%s]' % i_t.get_json())
        except IntegrityError:
            print ('add ingre type error')

    return HttpResponse('[]')


def add_meal_type(request):
    if request.method != 'POST':
        return HttpResponse('[]')

    if not request.user.is_authenticated():
        return HttpResponse('[]')

    if 'name' not in request.POST or 'desc' not in request.POST:
        return HttpResponse('[]')

    if len(request.POST['name'])!=0:
        try:
            m_t, _ = MealType.objects.get_or_create( Name = request.POST['name'], Creator = request.user, Description = request.POST['desc'])
            m_t.save()
            if _:
                return HttpResponse('[%s]' % m_t.get_json())
        except IntegrityError:
            print ('add meal type error')

    return HttpResponse('[]')


def add_ingre(request):
    if request.method != 'POST':
        return HttpResponse('[]')

    if not request.user.is_authenticated():
        return HttpResponse('[]')

    if 'name' not in request.POST or 'desc' not in request.POST or 'type' not in request.POST:
        return HttpResponse('[]')

    if len(request.POST['name'])!=0:
        ingre, _ = Ingredient.objects.get_or_create( Name = request.POST['name'], Creator = request.user, Description = request.POST['desc'])
        ingre.Types.clear()
        for id in json.loads(request.POST['type']):
            ingre.Types.add(IngredientType.objects.get(id= id))

        ingre.save()

        if _:
            return HttpResponse('[%s]' % ingre.get_json())

    return HttpResponse('[]')

def add_recipe(request):
    if request.method != 'POST':
        return HttpResponse('[]')

    if not request.user.is_authenticated():
        return HttpResponse('[]')

    if 'recipe' not in request.POST:
        return HttpResponse('[]')

    recipe = json.loads(request.POST['recipe'])

    if len(recipe['r_name']) == 0:
        return HttpResponse('{"com": "SET NAME!"}')

    if len(recipe['r_desc']) == 0:
        return HttpResponse('{"com": "SET DESCRITION."}')

    if recipe['r_time'] == 0:
        return HttpResponse('{"com": "SET TIME!"}')

    if recipe['r_diff'] == 0:
        return HttpResponse('{"com": "SET DIFFICULTY!"}')

    if len(recipe['ingre_list']) == 0:
        return HttpResponse('{"com": "ADD INGREDIENTS!"}')

    if len(recipe['types']) == 0:
        return HttpResponse('{"com": "ADD TIME!"}')

    meal = Meal(Name = recipe['r_name'],
                Creator = request.user,
                Description = recipe['r_desc'],
                Difficulty = recipe['r_diff'],
                Time = recipe['r_time'])  
    meal.save()

    try:
        for id in recipe['types']:
            meal.Types.add(MealType.objects.get(id= id))

        for f_i in recipe['ingre_list']:
            food_ing, _ = FoodIngredient.objects.get_or_create(Ingredient_id = f_i['ingre_id'], Unit_id = f_i['unit_id'],Number = f_i['number'])
            meal.Ingredients.add(food_ing)

    except IntegrityError as e:
        meal.delete()
        return HttpResponse('{"com": "SOMETHON WENT WRONG!"}')

    return redirect('{"com": "EVERYTHING OK, RECIPE CORRECTLY."}')