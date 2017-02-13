from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from forum.models import Topic, Post
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


topic_count = 20
post_count = 20;

def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    page = 1
    if 'page' in request.GET:
        page = request.GET['page']

    topics_all = Topic.objects.all()

    topics = Paginator(topics_all, topic_count)

    try:
        topics = topics.page(page)
    except EmptyPage as e:
        topics = topics.page(1) 
        page = 1

    pages = []
        
    if topics.has_previous():
        pages.append(topics.previous_page_number())

    if topics.has_other_pages():
        pages.append(page)

    if topics.has_next():
        pages.append(topics.next_page_number())

    return render(request, 'index.html', {'content': render(request, 'forum.html', {'topics': topics, 'pages': pages, 'current_page': page}).content}, content_type='application/xhtml+xml')

def add_new_topic(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    if request.method != 'POST':
        return redirect('/forum')

    topic = Topic(Name = request.POST['name'], Description = request.POST['desc'], Creator = request.user)
    topic.save()

    return redirect('/forum/%s/' % topic.id)

def add_new_post(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    if request.method != 'POST':
        return HttpResponseRedirect('/')

    try:
        if len(request.POST['content'])==0:
            return HttpResponseRedirect('/forum/%s/' % request.POST['topic_id'])

        topic = Topic.objects.get(id = request.POST['topic_id'])

        post = Post(Author = request.user, Topic = topic, Content = request.POST['content'])
        post.save()

        posts = Paginator(topic.post_set.all(), post_count)
        return redirect('/forum/%s/?page=%s' %(topic.id, posts.num_pages))
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/forum/%s/' % request.POST['topic_id'])
    except IntegrityError:
        return HttpResponseRedirect('/forum/%s/' % request.POST['topic_id'])



def topic(request, topic_id):
    if not request.user.is_authenticated():
        return redirect('/login/')

    try:
        topic = Topic.objects.get(id = topic_id)

        page = 1
        if 'page' in request.GET:
            page = request.GET['page']

        posts = Paginator(topic.post_set.all(), post_count)

        try:
            posts =posts.page(page)
        except EmptyPage as e:
            posts = posts.page(1) 
            page = 1

        pages = []
        
        if posts.has_previous():
            pages.append(posts.previous_page_number())

        if posts.has_other_pages():
            pages.append(page)

        if posts.has_next():
            pages.append(posts.next_page_number())

        return render(request, 'index.html', {'content': render(request, 'topic.html', {'topic': topic, 'posts': posts, 'pages': pages, 'current_page': page}).content}, content_type='application/xhtml+xml')
    except ObjectDoesNotExist:
        return redirect('/forum')
        
