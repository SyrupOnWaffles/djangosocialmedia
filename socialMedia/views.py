from django.shortcuts import render
from django.http import HttpResponseRedirect
from socialMedia.models import Post, UserProfile, Reply
from socialMedia.forms import CanvasForm
import urllib.request
import random
import string

# Create your views here.
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    replys = Reply.objects.filter(post=post).order_by("-created_on")

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

# Create your views here.
def post_homepage(request):
    posts = Post.objects.all().order_by("-created_on")
    # replys = Reply.objects.filter(post=post)

    # comments = Comment.objects.filter(post=post)
    context = {
        "posts": posts,
        # "replys": replys,
    }

    return render(request, "homepage.html", context)

# Create your views here.
def create_post(request):
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
            return HttpResponseRedirect("/")
    
    context = {
        "canvasForm": CanvasForm()
    }
    return render(request, "create_post.html", context)
