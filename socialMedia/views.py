from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator
from socialMedia.models import Post, UserProfile, Reply, Like
from socialMedia.forms import CanvasForm
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
    profile = UserProfile.objects.get( pk=pk)
    posts = Post.objects.filter(created_by=pk).order_by('-created_on')

    context = {
        "profile": profile,
        "posts": posts,
    }
    return render(request, "profile_detail.html", context)

def post_homepage(request):
    page=1
    order_by="created_on"

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)
    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    if('sort_by' in parsed_url):
        order_by=parsed_url['sort_by'][0]
    print(parsed_url)
    posts = Paginator(Post.objects.all().annotate(like_count=Count('likes')).order_by('likes'), 50)
    context = {
        "posts": posts.page(page),
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