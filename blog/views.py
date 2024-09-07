from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):
    allPosts = Post.objects.all()
    params = {'allPosts' : allPosts}
    return render(request, 'blog/index.html', params)

def blogpost(request, id):
    currentPost = Post.objects.filter(post_id = id).first()
    return render(request, 'blog/blogpost.html', {'post' : currentPost})
