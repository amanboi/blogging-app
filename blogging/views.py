from django.shortcuts import render, HttpResponse
from blogging.models import Post

# Create your views here.
def bloggingHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blogging/blog_home.html', context)
    # return HttpResponse('This is blog home. All blog post will be kept here.')


def bloggingPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post' : post}
    # return HttpResponse(f'This is blogPost: {slug}')
    return render(request, 'blogging/blogpost.html', context)  
