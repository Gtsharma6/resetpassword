from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import UserLoginForm,PostForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate,logout
from .models import CustomUser,Post
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.


def home(request):
    return render(request,'blog/home.html')

def log_out(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = UserLoginForm()
        return render(request, 'blog/signup.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    print(posts)
    return render(request, 'blog/post_list.html', {"posts" : posts })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #print(post.author)
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
    
    else:

        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(post.author)
    user = request.user
    print(user)
    return render(request, 'blog/post_detail.html', {'post': post,"user":user})

def myblogs(request):
    user = request.user
    print(user)
    post = Post.objects.filter(author=user)
    return render(request, 'blog/post_list.html', {'post': post,"user":user})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_list')
            
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_new.html', {'form': form})