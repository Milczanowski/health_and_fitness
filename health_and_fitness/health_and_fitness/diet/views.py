from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout as _logout, authenticate, login as _login
from diet.models import Diets, Meal, MealComment
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

diets_count = 20
meals_count = 20

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

    diets_all = Diets.objects.all()
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
    pass

def meals(request):
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']

    meals_all = Meal.objects.all()
    meals = Paginator(meals_all, meals_count)

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


    return render(request, 'index.html', {'content': render(request, 'meals.html', { 'meals': meals, 'pages': pages, 'current_page': page}).content}, content_type='application/xhtml+xml')


def meal(request, meal_id):
    try:
        meal = Meal.objects.get(id = meal_id)

        return render(request, 'index.html', {'content': render(request, 'meal.html', { 'meal': meal}).content}, content_type='application/xhtml+xml')
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
    