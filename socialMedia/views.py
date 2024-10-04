from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator
from socialMedia.models import Post, UserProfile, Reply, Like, ReplyLike, Follow
from socialMedia.forms import CanvasForm
from django.db.models.functions import Now
import urllib.request
import random
import string
from urllib.parse import urlparse, parse_qs

# search
def profile_search(request, username):
    page=1

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    
    profiles = UserProfile.objects.filter(user__username__contains=username)
    profiles = Paginator(profiles, 100)

    context = {
        "page" : page,
        "max_page" : profiles.num_pages,
        "profiles": profiles.page(page),
    }
    return render(request, "profile_search.html", context)

# post displays
def post_detail(request, pk):
    order_by="-like_count"
    url_sort_by="best"
    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('sort_by' in parsed_url):
        if(parsed_url['sort_by'][0]=="best"):
            order_by="-like_count"
            url_sort_by="best"
        elif(parsed_url['sort_by'][0]=="worst"):
            order_by="like_count"
            url_sort_by="worst"
        elif(parsed_url['sort_by'][0]=="new"):
            order_by="-created_on"
            url_sort_by="new"

    post = Post.objects.get(pk=pk)
    replys = Reply.objects.filter(post=post).annotate(like_count=Count('reply_likes')+1).order_by(order_by)

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
        "replys":replys,
        "url_sort_by" :url_sort_by,
        "canvasForm": CanvasForm()
    }
    return render(request, "post_detail.html", context)

def profile_detail(request, pk):
    profile = UserProfile.objects.get(pk=pk)

    page=1
    order_by="-like_count"
    url_sort_by="best"

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    if('sort_by' in parsed_url):
        if(parsed_url['sort_by'][0]=="best"):
            order_by="-like_count"
            url_sort_by="best"
        elif(parsed_url['sort_by'][0]=="worst"):
            order_by="like_count"
            url_sort_by="worst"
        elif(parsed_url['sort_by'][0]=="new"):
            order_by="-created_on"
            url_sort_by="new"
    posts = Post.objects.filter(created_by=pk)
    posts = Paginator(posts.annotate(like_count=Count('likes')+1).order_by(order_by), 10)
    
    context = {
        "profile" : profile,
        "posts": posts.page(page),
        "url_sort_by":url_sort_by,
        "sort_by" :order_by,
        "page" : page,
        "max_page" : posts.num_pages,
    }
    return render(request, "profile_detail.html", context)

def post_homepage(request):
    page=1
    order_by="-like_count"
    url_sort_by="best"

    parsed_url = parse_qs(urlparse(request.build_absolute_uri()).query)    
    if('page' in parsed_url):
        page=parsed_url['page'][0]
    if('sort_by' in parsed_url):
        if(parsed_url['sort_by'][0]=="best"):
            order_by="-like_count"
            url_sort_by="best"
        elif(parsed_url['sort_by'][0]=="worst"):
            order_by="like_count"
            url_sort_by="worst"
        elif(parsed_url['sort_by'][0]=="new"):
            order_by="-created_on"
            url_sort_by="new"

    posts = Post.objects.all()
    posts = Paginator(posts.annotate(like_count=Count('likes')).order_by(order_by), 10)
    
    context = {
        "posts": posts.page(page),
        "url_sort_by" :url_sort_by,
        "page" : page,
        "max_page" : posts.num_pages
    }
    return render(request, "homepage.html", context)

# drawing
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

def create_pfp(request):
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
            user = UserProfile.objects.get(pk=request.user.pk)
            user.profile_picture = f"{name}.png"
            user.save()

            return HttpResponseRedirect(reverse(profile_detail,args=[request.user.pk]))
    
    context = {
        "canvasForm": CanvasForm()
    }
    return render(request, "create_pfp.html", context)

def create_bio(request):
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
            user = UserProfile.objects.get(pk=request.user.pk)
            user.bio_picture = f"{name}.png"
            user.save()

            return HttpResponseRedirect(reverse(profile_detail,args=[request.user.pk]))
    
    context = {
        "canvasForm": CanvasForm()
    }
    return render(request, "create_bio.html", context)

# delete
def delete_post(request,pk):
    if(request.user.pk != Post.objects.get(pk=pk).created_by.pk):
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        Post.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('profile_detail',args=[request.user.pk]))

# delete
def delete_reply(request,pk):
    mother_post = Reply.objects.get(pk=pk).post

    if(request.user.pk != Reply.objects.get(pk=pk).created_by.pk):
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        Reply.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('post_detail',args=[mother_post.pk]))

# follows
def profile_follow(request, pk):
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        if request.user.is_authenticated is True:
            if request.user.pk != pk:
                query = Follow.objects.filter(created_by=request.user.pk)
                if query.exists():
                    query.delete()
                else:
                    Follow.objects.create(follow_to=UserProfile.objects.get(pk=pk),created_by=UserProfile.objects.get(pk=request.user.pk))
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)

def profile_get_followers(request, pk):
    return HttpResponse(UserProfile.objects.get(pk=pk).followers.count())

# likes
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

def reply_like(request, pk):
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        if request.user.is_authenticated is True:
            query = ReplyLike.objects.filter(reply=pk,created_by=request.user.pk)
            if query.exists():
                query.delete()
            else:
                ReplyLike.objects.create(reply=Reply.objects.get(pk=pk),created_by=UserProfile.objects.get(pk=request.user.pk))
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

def post_get_likes(request, pk):
    return HttpResponse(Post.objects.get(pk=pk).likes.count())

def reply_get_likes(request, pk):
    return HttpResponse(Reply.objects.get(pk=pk).reply_likes.count())