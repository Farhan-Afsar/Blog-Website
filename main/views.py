from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {
        'post': post
    })

def contact(request):
    return render(request, 'blog/contact.html')