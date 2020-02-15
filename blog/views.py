from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import UserLoginForm,PostForm,SubscriberForm,CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate,logout
from .models import CustomUser,Post,Comment
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from myproject.settings import EMAIL_HOST_USER
from django.db.models import Count

# Create your views here.


def home(request):
    return render(request,'blog/home.html')

def log_out(request):
    logout(request)
    return redirect('blog:home')

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
     # list of active parent comments
    comments = post.comments.filter(active=True, reply__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            reply_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                reply_id = int(request.POST.get('reply_id'))
            except:
                reply_id = None
            # if parent_id has been submitted get parent_obj id
            if reply_id:
                reply_obj = Comment.objects.get(id=reply_id)
                # if parent object exist
                if reply_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.reply = reply_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return redirect('blog/post_detail',pk)
    else:
        comment_form = CommentForm()
    
    return render(request,'blog/post_detail.html',{'post':post,'comments': comments,
                   'comment_form': comment_form})



    """print(post.author)
    user = request.user
    print(user)
    return render(request, 'blog/post_detail.html', {'post': post,"user":user})"""



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


#how to send html template through email
def subscriber(request):
    form = SubscriberForm(request.POST)
    if request.method == "POST":
       
        if form.is_valid():
            email = form.cleaned_data['email']
            message_html = render_to_string('blog/email_sent.html')
            #plain_message = strip_tags(html_message)
            subject = form.cleaned_data['subject']
            #try:
            #in this way email format send in template
            send_mail(subject,recipient_list=[email],from_email=EMAIL_HOST_USER,message=subject,html_message=message_html)
            #except BadHeaderError:
                #return HttpResponse('Invalid header found.')
            return HttpResponse("Sucess!Thank you for subscribe")
    return render(request, "blog/subscribe.html", {'form': form})

"""def sucess(request):
    return HttpResponse("Sucess!Thank you for subscribe")"""

"""def add_comment_to_post(request,pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():

            Comment = form.save(commit=False)
            Comment.post = post
            Comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form}) 


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=Comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=Comment.post.pk)"""



    
            