from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator
from socialMedia.models import Post, UserProfile, Reply, Like
from socialMedia.forms import CanvasForm
from django.db.models.functions import Now
import urllib.request
import random
import string
from urllib.parse import urlparse, parse_qs

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    replys = Reply.objects.filter(post=post).order_by("-created_on")
    liked = Like.objects.filter(created_by=request.user.pk)

    form = CanvasForm()
    if request.method == "POST":
        form = CanvasForm(request.POST)
        if form.is_valid():
            name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=64))
            response = urllib.request.urlopen(form.cleaned_data["body"])
            with open(f'media/{name}.png', 'wb') as f:
                f.write(response.file.read())
            reply = Reply(
                created_by= UserProfile.objects.get(user=request.user),
                body = f"{name}.png",
                post=post,
            ).save()
            return HttpResponseRedirect(request.path_info)
    
    context = {
        "post": post,
        "replys": replys,
        "liked" : liked,
        "canvasForm": CanvasForm()
    }
    return render(request, "post_detail.html", context)

def profile_detail(request, pk):
    profile = UserProfile.objects.get(pk=pk)

    page=1
    order_by="-like_count"

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    if('sort_by' in parsed_url):
        if(parsed_url['sort_by'][0]=="best"):
            order_by="-like_count"
        elif(parsed_url['sort_by'][0]=="worst"):
            order_by="like_count"
        elif(parsed_url['sort_by'][0]=="new"):
            order_by="-created_on"

    posts = Post.objects.filter(created_by=pk)
    posts = Paginator(posts.annotate(like_count=Count('likes')+1).order_by(order_by), 5)
    
    context = {
        "profile" : profile,
        "posts": posts.page(page),
        "sort_by" :order_by,
        "page" : page,
    }
    return render(request, "profile_detail.html", context)

def post_homepage(request):
    page=1
    order_by="-like_count"

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    if('sort_by' in parsed_url):
        if(parsed_url['sort_by'][0]=="best"):
            order_by="-like_count"
        elif(parsed_url['sort_by'][0]=="worst"):
            order_by="like_count"
        elif(parsed_url['sort_by'][0]=="new"):
            order_by="-created_on"

    posts = Post.objects.all()
    posts = Paginator(posts.annotate(like_count=Count('likes')+1).order_by(order_by), 5)
    
    context = {
        "posts": posts.page(page),
        "sort_by" :order_by,
        "page" : page,
    }
    return render(request, "homepage.html", context)

def create_post(request):
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("/")
    form = CanvasForm()
    if request.method == "POST":
        form = CanvasForm(request.POST)
        if form.is_valid():
            name = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=64))
            response = urllib.request.urlopen(form.cleaned_data["body"])
            with open(f'media/{name}.png', 'wb') as f:
                f.write(response.file.read())
            post = Post(
                created_by= UserProfile.objects.get(user=request.user),
                body = f"{name}.png",
            ).save()
            return HttpResponseRedirect(reverse(post_detail,args=[Post.objects.get(body=f"{name}.png").pk]))
    
    context = {
        "canvasForm": CanvasForm()
    }
    return render(request, "create_post.html", context)

def post_like(request, pk):
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        if request.user.is_authenticated is True:
            query = Like.objects.filter(post=pk,created_by=request.user.pk)
            if query.exists():
                query.delete()
            else:
                Like.objects.create(post=Post.objects.get(pk=pk),created_by=UserProfile.objects.get(pk=request.user.pk))
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

def post_get_likes(request, pk):
    return HttpResponse(Post.objects.get(pk=pk).likes.count())