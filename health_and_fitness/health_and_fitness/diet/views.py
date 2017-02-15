from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout as _logout, authenticate, login as _login
from diet.models import Diet, Meal, MealComment, DietComment, Ingredient, IngredientComment,  MealType
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

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

        return render(request, 'index.html', {'content': render(request, 'diet.html', { 'diet': diet, 'rating_enable': diet.rating_enable(request.user) }).content}, content_type='application/xhtml+xml')
    except ObjectDoesNotExist as e:
        return redirect('/')

class Search_Param():
    
    def __init__(self):
        self.search_param = dict()

    def clear(self, user_id):
        self.search_param[int(user_id)] = dict()

    def add(self, user_id, post_param):
        self.search_param[int(user_id)] = dict()

        if 'type' in post_param:
            self.search_param[int(user_id)]['type'] = post_param['type']

        if 'max_time' in post_param:
            self.search_param[int(user_id)]['max_time'] = post_param['max_time']

        if 'max_diff' in post_param:
            self.search_param[int(user_id)]['max_diff'] = post_param['max_diff']

        if 'min_rat' in post_param:
            self.search_param[int(user_id)]['min_rat'] = post_param['min_rat']

        if 'ingre' in post_param:
            self.search_param[int(user_id)]['ingre'] = post_param['ingre']

    def get_meals(self, user_id):
        meals = Meal.objects.all()

        if int(user_id) in self.search_param:
            if  'max_time' in  self.search_param[int(user_id)]:
                if int(self.search_param[int(user_id)]['max_time'])!= 0:
                    meals = meals.filter(Time__lte =int(self.search_param[int(user_id)]['max_time']))

            if  'max_diff' in  self.search_param[int(user_id)]:
                if int(self.search_param[int(user_id)]['max_diff'])!= 0:
                    meals = meals.filter(Difficulty__lte =int(self.search_param[int(user_id)]['max_diff']))

            if  'min_rat' in  self.search_param[int(user_id)]:
                if int(self.search_param[int(user_id)]['min_rat'])!= 0:
                    meals = meals.filter(c_ratting__gte =int(self.search_param[int(user_id)]['min_rat']))

            if  'type' in  self.search_param[int(user_id)]:
                meals = meals.filter(Types__in= self.search_param[int(user_id)]['type'])

            if  'ingre' in  self.search_param[int(user_id)]:
                meals = meals.filter(Ingredients__Ingredient__in = self.search_param[int(user_id)]['ingre'])

        return meals


search_param = Search_Param()

def meals(request):
    page = 1

    if request.method == 'GET':
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            search_param.clear(request.user.id)
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

        return render(request, 'index.html', {'content': render(request, 'meal.html', { 'meal': meal,  'rating_enable': meal.rating_enable(request.user) }).content}, content_type='application/xhtml+xml')
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
