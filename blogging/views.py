from django.shortcuts import render, HttpResponse, redirect
from blogging.models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def bloggingHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blogging/blog_home.html', context)
    # return HttpResponse('This is blog home. All blog post will be kept here.')


def bloggingPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    context = {'post' : post, 'comments': comments, 'user':request.user}
    # return HttpResponse(f'This is blogPost: {slug}')
    return render(request, 'blogging/blogpost.html', context)  




def postComment(request):
    if request.method=='POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        
        comment = BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
   
    return redirect(f"/blogging/{post.slug}")
